# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:47:25 2020

@author: Administrator
"""
#References
#https://www.learndatasci.com/tutorials/sentiment-analysis-reddit-headlines-pythons-nltk/

import requests
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from googlesearch import search
import nltk
from nltk.corpus import stopwords #nltk.download('stopwords') if unavailable
from nltk.tokenize import word_tokenize # nltk.download('punkt')  if unavailable
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import string
import pandas as pd

# to search 
query = "Osama Bin Laden"

class media_analyzer():
    

    def __init__(self,query,number_results):
        self.query = query
        self.number_of_results = number_results
 
    # function to extract links to google pages
    def link_extractor (self):
        self.html_link = []
        query = self.query
        numb = self.number_of_results
        for j in search(query, tld="com", num=numb, stop=numb, pause=4):
            self.html_link.append(j)
        return self.html_link
    
    # function to extract text from search pages
    def text_extractor (self,source_list): # takes in list of html links
        self.text_list = []
        for link in source_list:
            if requests.get(link).status_code == 200:
                soup = BeautifulSoup(requests.get(link).text, 'html.parser')
                page_text = soup.find_all('p')
                text = ""
                for element in page_text:
                    if element.text != "":
                        text += element.text
                        text += " "
                self.text_list.append(text)
        return self.text_list # returns a list of teext parsed from searched html links
    # function to remove punctuation, remove stopwords, and tokenize string content to words
    @staticmethod
    def cleaner(review): # takes in string
        stop_words = set(stopwords.words('english'))
        word_list = word_tokenize(review)
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in word_list]
        text = ""
        for word in stripped:
            if not word in stop_words:
                text += word
                text += " "
        return text  # retunrs string
    
    # function for sentiment analysis using NLTK's inbult sentiment analyzer
    @classmethod
    def polarity_calculator(cls,string_data): # takes in string
        sia = SIA()
        strng = cls.cleaner(string_data)
        pol_score = sia.polarity_scores((strng))
        pol_score['article'] = string_data
        return pol_score  #returns dict
    
    # funtion to generate the new score i.e good media or negative media coverage on the bases of search history 
    @classmethod
    def entity_score(cls,score_list):# takes in list
        df = pd.DataFrame.from_records(score_list)
        df['label'] = 0
        df.loc[df['compound'] > 0.2, 'label'] = 1
        df.loc[df['compound'] < -0.2, 'label'] = -1
        gk = df.groupby('label')
        score = len(gk.get_group(1)) - len(gk.get_group(-1))
        #entity = media_analyzer(self.query,self.number_results,self.entity_score)
        return score
        
        







import flask

app = flask.Flask(__name__)           # a Flask object


@app.route('/entity_search')
def ask_entity():
    return flask.render_template('entity_question.html')

@app.route('/details', methods=['POST', 'GET'])
def entity_analysis():
    entity_name =    flask.request.form.get('id')     # from a POST (form with 'method="POST"')
    no_id = flask.request.args.get('no_id')  # from a GET (URL)

    if entity_name:
        inst = media_analyzer(entity_name,20)
        out_1 = inst.link_extractor()
        out_2 = inst.text_extractor(out_1)
        out_3 = []
        for i in out_2:
            score = media_analyzer.polarity_calculator(i)
            out_3.append(score)
        final_score = media_analyzer.entity_score(out_3)
        
        #emp_details = media_analyzer.
        msg = flask.render_template('results_template.html', obj = inst, score = final_score)
        #msg = "Details" + "\n" + emp_details.eid + "\n" + emp_details.fname + "\n" + emp_details.lname + "\n" + emp_details.state
    elif no_id:
        msg = 'No Object Details.'
    else:
        raise ValueError('\nraised error:  no "name" or "no_name" params passed in request')

    return '<PRE>{}</PRE>'.format(msg)
if __name__ == '__main__':
    app.run(debug=True, port=5000)    # app starts serving in debug mode on port 5000


