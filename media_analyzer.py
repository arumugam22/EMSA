import requests
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from googlesearch import search
import nltk
#https://stackoverflow.com/questions/36516697/not-able-to-install-nltk-data-on-django-app-on-elastic-beanstalk/36526192#36526192 for bringing in the #ntlk data on AWS beanstalj environment
try:
    nltk.download('punkt', download_dir='/opt/python/current/app')
    nltk.download('stopwords', download_dir='/opt/python/current/app')
    nltk.download('vader_lexicon', download_dir='/opt/python/current/app')
except:
    nltk.download('punkt')
    nltk.download('vader_lexicon')
    nltk.download('stopwords')

from nltk.corpus import stopwords #nltk.download('stopwords') if unavailable
from nltk.tokenize import word_tokenize # nltk.download('punkt')  if unavailable
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import string
import pandas as pd
import wikipedia
from pandas.io.html import read_html
#from docx import newdocument
#import docx
from fpdf import FPDF
import pymysql




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
                        text += (element.text).encode("ascii", errors="ignore").decode(errors="ignore").lower()
                        text += " "
                self.text_list.append(text)
            else:
                pass
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
    
    #function to generate text summary statistics
    @classmethod
    def text_summary(cls,text_list):# takes in a list
        wordcount = {}
        for i in text_list:
            strng = cls.cleaner(i.lower())  #takes string,returns string
            for word in strng.lower().split():
                if word not in wordcount:
                    wordcount[word] = 1
                else:
                    wordcount[word] += 1
        return sorted(wordcount.items(),key=lambda kv:(kv[1], kv[0]), reverse = True)
    
    @classmethod
    def TF_ML_ABC_Keywords(cls):
        ABC_keywords = []
        TF_keywords = []
        ML_keywords = []
        f = open("ABC_Keywords.txt", "r",errors = 'ignore')
        for x in f:
            ABC_keywords.append(((cls.cleaner(x)).lower()).strip())
        f = open("AML_Keywords.txt", "r",errors = 'ignore')
        for x in f:
            ML_keywords.append(((cls.cleaner(x)).lower()).strip())
        f = open("TF_Keywords.txt", "r",errors = 'ignore')
        for x in f:
            TF_keywords.append(((cls.cleaner(x)).lower()).strip())
        return ABC_keywords,TF_keywords,ML_keywords
    
    @classmethod
    def text_summary_keywords(cls,text_list,keyword_list):# takes in a list
        wordcount = {}
        for i in text_list:
            strng = cls.cleaner(i.lower())  #takes string,returns string
            for word in strng.lower().split():
                if word in keyword_list: 
                    if word not in wordcount:
                        wordcount[word] = 1
                    else:
                        wordcount[word] += 1
        return sorted(wordcount.items(),key=lambda kv:(kv[1], kv[0]), reverse = True)
    
    
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
        keys_out = gk.groups.keys()
        
        #ow_o = len(gk.get_group(1))
        #ow_t = len(gk.get_group(-1))
        
        if 1 in keys_out and -1 in keys_out:
           score = len(gk.get_group(1)) - len(gk.get_group(-1))
        elif 1 in keys_out:
           score = len(gk.get_group(1))
        elif -1 in keys_out:
           score = len(gk.get_group(-1))
        else:
           score = 0
        #entity = media_analyzer(self.query,self.number_results,self.entity_score)
        return score #,ow_o,ow_t
