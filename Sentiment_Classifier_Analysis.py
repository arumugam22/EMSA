# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 14:59:03 2020

@author: abhis
references:
#http://akashsenta.com/blog/sentiment-analysis-with-vader-with-python/
#Scoring Methodology https://github.com/cjhutto/vaderSentiment#about-the-scoring
https://www.learndatasci.com/tutorials/predicting-reddit-news-sentiment-naive-bayes-text-classifiers/
https://www.nltk.org/howto/sentiment.html 
vader vs NLTK   
https://medium.com/analytics-vidhya/simplifying-social-media-sentiment-analysis-using-vader-in-python-f9e6ec6fc52f
"""


# Load and prepare the dataset
import nltk
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords #nltk.download('stopwords') if unavailable
from nltk.tokenize import word_tokenize
import random
import string
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix


documents = [(list(movie_reviews.words(fileid)), category)
              for category in movie_reviews.categories()
              for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)



# cleaning up the word features
def cleaner(review): # takes in string
    stop_words = set(stopwords.words('english'))
    table = str.maketrans('', '', string.punctuation)
    stripped = review.translate(table)
    text = ""
    if not stripped in stop_words:
        text = stripped 
    return text  # retunrs string



all_words_1 = []

for w in movie_reviews.words():
    if cleaner(w.lower()):
        all_words_1.append(w.lower())

# Define the feature extractor
        
all_words = nltk.FreqDist(w.lower() for w in all_words_1)
word_features = list(all_words)[:2000] # selecting the top 2000 word features



def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

# Train Naive Bayes classifier
featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]

#classifier = nltk.NaiveBayesClassifier.train(train_set)

# Evaluating the classifier accuracy
#print(nltk.classify.accuracy(classifier, test_set))

trainer = NaiveBayesClassifier.train
classifier = sentim_analyzer.train(trainer, train_set)
#Training classifier
for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
    print('{0}: {1}'.format(key, value))
"""
Evaluating NaiveBayesClassifier results...
Accuracy: 0.8
F-measure [neg]: 0.8113207547169812
F-measure [pos]: 0.7872340425531915
Precision [neg]: 0.7818181818181819
Precision [pos]: 0.8222222222222222
Recall [neg]: 0.8431372549019608
Recall [pos]: 0.7551020408163265
"""
#Vader Classifier
#http://akashsenta.com/blog/sentiment-analysis-with-vader-with-python/


    
def cleaner_sentence(review): # takes in string
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

def polarity_calculator(string_data): # takes in string
    sia = SIA()
    strng = cleaner_sentence(string_data)
    pol_score = sia.polarity_scores((strng))
    pol_score['article'] = string_data
    return pol_score  #returns dict
    
# funtion to generate the new score i.e good media or negative media coverage on the bases of search history
#Scoring Methodology https://github.com/cjhutto/vaderSentiment#about-the-scoring
    
data_corpora = [[movie_reviews.raw(fileid),fileid[:3]] for fileid in movie_reviews.fileids()]

score_list = []
label =[]
for i in data_corpora:
    score_list.append(polarity_calculator(i[0]))
    label.append(i[1])

df = pd.DataFrame(score_list)
df['label'] = label

df['score'] = df['compound'].apply(lambda score: 'pos' if score > 0.05 else ('neg' if score < 0.05 else score ))
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
accuracy_score(df['label'],df['score']) #0.61
print(classification_report(df['label'],df['score']))

"""
              precision    recall  f1-score   support

         neg       0.70      0.38      0.50      1000
         pos       0.58      0.84      0.68      1000

    accuracy                           0.61      2000
   macro avg       0.64      0.61      0.59      2000
weighted avg       0.64      0.61      0.59      2000
"""
