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



class database_operations():
    
    def database_read(self,entity_name,page):
        #db_details
        host="database-a.cx7qexz64alu.us-west-2.rds.amazonaws.com"
        port=3306
        dbname="EMSAdatabase"
        user="AbhishekKalra"
        password="Abhishek_88"
        
        conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname )
        
        #mycursor = conn.cursor()
        read_query = pd.read_sql(("Select entity_name,sentiment,common_keyword,ML_keywords,ABC_Keywords,TF_keywords,max(score) final_ccore from EMSAdatabase.EMSA_SEARCH_HISTORY where entity_name = ? and number_of_pages = ? group by entity_name,common_keyword,ML_keywords,ABC_Keywords,TF_keywords; ",(entity_name,page)), con=conn)
        
        if read_query:
            ABC_list = read_query[4]
            ML_list = read_query[4]
            TF_list = read_query[4]
            common_keyword = read_query[4]
            #final_sentiment = read_query[4]
            final_score = read_query[4]
        else:
            pass
        
        return ABC_list, ML_list, TF_list, common_keyword, final_score
    
    @classmethod
    def database_write(cls,entity_name,page,url,final_score,common_keyword,ML_list,ABC_list,TF_list):
        #db_details
        host="database-a.cx7qexz64alu.us-west-2.rds.amazonaws.com"
        port=3306
        dbname="EMSAdatabase"
        user="AbhishekKalra"
        password="XXXXXXXX"
        
        conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname )
        mycursor = conn.cursor()
        mycursor.execute ("CREATE TABLE IF NOT EXISTS EMSAdatabase.EMSA_SEARCH_HISTORY (rowid int AUTO_INCREMENT PRIMARY KEY, Entity_Name varchar(255),page int, url varchar(255),Score int,  common_keywords varchar(255),ML_keywords varchar(255),ABC_keywords varchar(255),TF_keywords varchar(255));")
        sql = "INSERT INTO EMSAdatabase.EMSA_SEARCH_HISTORY ( entity_name,page,url,score,common_keywords,ML_keywords,ABC_keywords,TF_keywords) VALUES (%s, %s,%s,%s,%s,%s,%s,%s)"
        val = (entity_name,page,url,final_score,common_keyword,ML_list,ABC_list,TF_list)
        mycursor.execute(sql, val)
        conn.commit()
        #mycursor.execute("INSERT INTO EMSAdatabase.EMSA_SEARCH_HISTORY VALUES (?, ?, ?,?,?,?,?,?)", (entity_name,page,url,final_score,common_keyword,ML_list,ABC_list,TF_list))
