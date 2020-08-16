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



class case_narrative():
    # ASSIGN THE VARIABLES FROM MEDIA ANALYZER CLASS OUTPUT
    def __init__(self,entity_name,final_score,out_1,keyword_list,page,ABC_list,ML_list,TF_list):
        self.entity_name = entity_name
        self.final_score = final_score
        self.out_1 = out_1
        self.keyword_list = keyword_list
        self.page = page

  # EXTRACT THE PROFILE INFORMATION FROM WIKIPEDIA
        wiki_search = wikipedia.search(entity_name,10)

        if final_score > 0:
            sentiment = "Postitve"
            
        elif final_score < 0:
            sentiment = "Negative"
        
        elif final_score == 0:
            sentiment = "Neutral"
            

        ML_keyword = 'Fraud'
        selection = wiki_search[1]
        selection_page = wikipedia.page(selection)
        selection_url = selection_page.url
        page1 = selection_url

# EXTRACT INFOBOX FROM WIKIPEDIA
        try:
            malformed = read_html(page1, index_col=0, attrs={"class":"infobox"})
            malformed[0]
            Err = 'No'

        except ValueError:
            Err = 'yes'    
# CREATE THE CASE NARRATIVE WORD DOUCMENT AND PLACE THE PROFILE INFORMATION
        summ = (wikipedia.summary(selection, sentences = 2))
        
        pdf = FPDF(orientation = 'P', unit = 'mm', format='Letter')
        pdf.add_page()
        
        pdf.set_font("Arial", 'B',size = 18) 
        pdf.set_text_color(50, 143, 220)
        pdf.cell(200, 10, txt = "Case Narrative Template",ln = 1, align = 'C') 
        pdf.line(5.0,5.0,205.0,5.0)
        pdf.set_font("Arial", size = 15) 
        pdf.set_text_color(10, 10, 10)
        pdf.cell(200, 10, txt = "Entity Name : " + entity_name, ln = 2, align = 'C') 
        pdf.set_font("Arial", size = 12) 
        pdf.set_text_color(50, 143, 220)
        pdf.cell(200, 10, txt = "Introduction ", ln = 3, align = 'C') 
        pdf.set_text_color(10, 10, 10)
        pdf.multi_cell(0,10,summ)
        pdf.set_font("Arial", 'B',size = 10) 
        pdf.set_text_color(50, 143, 220)
        pdf.cell(200, 10, txt = "Entity Media analyser", ln = 18)
        pdf.set_text_color(10, 10, 10)
        pdf.cell(200, 10, txt = "Sentiment : "+ sentiment, ln = 19 ) 
        pdf.cell(200, 10, txt = "Final Score :" + str(final_score), ln = 20) 
        pdf.set_font("Arial", 'B',size = 10) 
        pdf.set_text_color(50, 143, 220)
        pdf.cell(200, 10, txt = "Top 5 Key words in the webpage", ln = 22 ) 
        pdf.set_text_color(10, 10, 10)
        # TOP 5 KEY WORD LIST FROM MEDIA ANALYSER CLASS    
        for i in keyword_list:
            pdf.multi_cell(0,10, (str(i)))

        pdf.set_text_color(50, 143, 220)
        pdf.cell(200, 10, txt = "Top 5 Money Laundering Key words in the webpage", ln = 28)
        pdf.set_text_color(10, 10, 10)
   # TOP 5 KEY WORD LIST FROM MEDIA ANALYSER CLASS    
        for i in ML_list:
            pdf.multi_cell(0,10, (str(i)))   

        pdf.set_text_color(50, 143, 220)
        pdf.cell(200, 10, txt = "Top 5 Terrorist Financing Key words in the webpage", ln = 34 )
        pdf.set_text_color(10, 10, 10)
   # TOP 5 KEY WORD LIST FROM MEDIA ANALYSER CLASS    
        for i in TF_list:
            pdf.multi_cell(0,10, (str(i)))            
  
        pdf.set_text_color(50, 143, 220)
        pdf.cell(200, 10, txt = "Top 5 Bribery & Corruption Key words in the webpage", ln = 46)
        pdf.set_text_color(10, 10, 10)
  
   # TOP 5 KEY WORD LIST FROM MEDIA ANALYSER CLASS    
        for i in ABC_list:
            pdf.multi_cell(0,10, (str(i)))

        pdf.set_text_color(50, 143, 220)
        
        pdf.cell(200, 10, txt = "Insights", ln = 65, align = 'C' )
        pdf.set_text_color(10, 10, 10)
        pdf.multi_cell(0,10,"Based on the below web page search, Focal entity "+entity_name+" appear in " +str(page)+ " web pages and overall sentiment is " + sentiment + " and sentiment final score is "+ str(final_score))
        pdf.set_text_color(50, 143, 220)
        pdf.cell(200,10,txt="Sources", ln = 70, align = 'C' )
        pdf.set_text_color(10, 10, 10)
       

        for i in  out_1:
            pdf.multi_cell(0,10, (i))         
        pdf.output("case_summary"+ entity_name +".pdf",'F') 

        """
        doc = docx.newdocument()
        doc.add_heading ('Case Narrative Template', 0)
        doc.add_heading ('Entity Name :' + entity_name, 2)
        doc.add_heading ('Introduction', 2)
        doc.add_paragraph(summ)

 # INFOBOX LOADED TO CASE NARRATIVE DOCUMENT

        if Err != 'yes':
            df = pd.DataFrame(malformed)
            t = doc.add_table(df.shape[0]+1, df.shape[1])
            # add the rest of the data frame
            for i in range(df.shape[0]):
                for j in range(df.shape[-1]):
                    t.cell(i+1,j).text = str(df.values[i,j])

        doc.add_heading ('Entity Media analyser', 2)
        doc.add_paragraph ('Sentiment :'+ sentiment)
        doc.add_paragraph ('Final Score :'+ str(final_score))
        doc.add_heading ('Top 5 Key words in the webpage',2)
  
   # TOP 5 KEY WORD LIST FROM MEDIA ANALYSER CLASS    
        for i in keyword_list:
            doc.add_paragraph (str(i))

        doc.add_heading ('Top 5 Money Laundering Key words in the webpage',2)
  
   # TOP 5 KEY WORD LIST FROM MEDIA ANALYSER CLASS    
        for i in ML_list:
            doc.add_paragraph (str(i))    

        doc.add_heading ('Top 5 Terrorist Financing Key words in the webpage',2)
  
   # TOP 5 KEY WORD LIST FROM MEDIA ANALYSER CLASS    
        for i in TF_list:
            doc.add_paragraph (str(i))             
  
        doc.add_heading ('Top 5 Bribery & Corruption Key words in the webpage',2)
  
   # TOP 5 KEY WORD LIST FROM MEDIA ANALYSER CLASS    
        for i in ABC_list:
            doc.add_paragraph (str(i)) 

        doc.add_paragraph ('Keywords releated to compliance: ' + ML_keyword)
        doc.add_heading ('Insights', 2)
        doc.add_paragraph('Based on the below web page search, Focal entity '+entity_name+' appear in ' +page+ ' web pages and overall sentiment is ' + sentiment + 'and sentiment final score is '+ str(final_score))
        doc.add_heading ('Sources', 2)

        for i in  out_1:
            doc.add_paragraph(i)

        doc.save('case_summary'+ entity_name +'.docx')
        """

