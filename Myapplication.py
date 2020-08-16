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

from case_narrative import case_narrative
from media_analyzer import media_analyzer
from database_operations import database_operations



# FLASK / REACT APP LOADING....
import flask
application = flask.Flask(__name__)           # a Flask object

@application.route('/', methods=['POST', 'GET']) #entity_search
def ask_entity():
    return flask.render_template('Landing_Template_fl.html')

@application.route('/details', methods=['POST', 'GET'])
def entity_analysis():

    entity_name = flask.request.form.get('ent')
    page = int(flask.request.form.get('page'))
    worddoc = flask.request.form.get('narrative')
    no_id = flask.request.form.get('no_id')  # from a GET (URL)
    media_analyzer(entity_name,page)
    
    if entity_name:
        page = page
        inst = media_analyzer(entity_name,page)
        out_1 = inst.link_extractor()
        out_2 = inst.text_extractor(out_1)
        out_3 = []
        for i in out_2:
            score = media_analyzer.polarity_calculator(i)
            out_3.append(score)
        final_score = int(media_analyzer.entity_score(out_3))
        
        
        if final_score > 0:
            sentiment = "Postitve"
            
        elif final_score < 0:
            sentiment = "Negative"
        
        elif final_score == 0:
            sentiment = "Neutral"

        keyword_list = (media_analyzer.text_summary(out_2)[:5])
        ABC_keywords,TF_keywords,ML_keywords = media_analyzer.TF_ML_ABC_Keywords()
        ABC_list = (media_analyzer.text_summary_keywords(out_2,ABC_keywords)[:5])
        TF_list = (media_analyzer.text_summary_keywords(out_2,TF_keywords)[:5])
        ML_list = (media_analyzer.text_summary_keywords(out_2,ML_keywords)[:5])

        
        if worddoc == 'Yes':
            #inst1 = case_narrative(entity_name,final_score,out_1,keyword_list,page,TF_list,ML_list,ABC_list)
            pass
        
        
        msg = flask.render_template('Result_Template.html', obj = inst, score = final_score, word_s = keyword_list, final_sentiment = sentiment,word_TF = TF_list,word_ML= ML_list, word_ABC = ABC_list)
        
        #writing to the database
        url_string = ""
        keyword_string = ""
        ML_string = ""
        ABC_string = ""
        TF_string = ""
        
        for i in out_1:
            url_string += str(i)
            url_string += ","
            
        for i in keyword_list:
            for a in i:
                keyword_string += str(a)
                keyword_string += " "
            keyword_string += ","
            
        for j in ML_list:     
            for a in j: 
                ML_string += str(a)
                ML_string += " "
            ML_string += ","
        
        for k in ABC_list:
            for a in k:
                ABC_string += str(a)
                ABC_string += " "
       
            ABC_string += ","
        
        for d in TF_list:
            for a in d:
                TF_string += str(a)
                TF_string += " "  
            TF_string += ","
    
        database_operations.database_write(entity_name,page,url_string,final_score,keyword_string,ML_string,ABC_string,TF_string)
    
    elif no_id:
        msg = 'No Object Details.'

    else:
        
        raise ValueError('\nraised error:  no "name" or "no_name" params passed in request')

    return '<PRE>{}</PRE>'.format(msg)

if __name__ == '__main__':
    application.run(debug=True, port=5000)    # app starts serving in debug mode on port 5000