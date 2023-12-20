##### Libraries #####

import pickle

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

import string
import re
import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.data.path.append('nltk_data')

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.linear_model import SGDClassifier

from sklearn.pipeline import Pipeline

##### Variables #####

punctuations = string.punctuation

stop_words = stopwords.words('english')
more_stopwords = ['u', 'im', 'c', 'ü', 'ur', '4', '2', 'dont', 'doin', 'ure']
stop_words = stop_words + more_stopwords

##### Helper functions #####

def remove_punctuations(text):
    for punctuation in punctuations:
        text = text.replace(punctuation, '')
    return text

def remove_numbers(text):
    text = re.sub(r'\d+', '', text)
    return text

def remove_links(text):
    text = re.sub(r'http\S+', '', text)
    return text

def remove_linebreaks(text):
    text = re.sub(r'\n', '', text)
    return text

def clean_text(text):
    text = remove_punctuations(text)
    text = remove_numbers(text)
    text = remove_links(text)
    text = remove_linebreaks(text)
    return text

def tokenize(text):
    return nltk.word_tokenize(text)

def remove_stopwords(text):
    text = ' '.join(word for word in text if word not in stop_words).split(' ')
    return text

lemmatizer = WordNetLemmatizer()

def lemmatize(text):
    text = ' '.join(lemmatizer.lemmatize(word) for word in text).split(' ')
    return text

def preprocess_text(text):
    text = clean_text(text)
    text = tokenize(text)
    text = remove_stopwords(text)
    text = lemmatize(text)
    return text

def dummy(doc):
    return doc

##### Preparing the data #####

df = pd.read_csv('data/spam.csv', encoding='latin-1')

df.dropna(how='any', inplace=True, axis=1)
df.columns = ['type', 'text']

# Binary target column
df['target'] = df['type'].map({'ham':0, 'spam':1})

# Preprocessing
df['tokenized_text'] = df['text'].apply(preprocess_text)

df['tokenized_text'] = df['tokenized_text'].apply(lambda x: ' '.join(x))

##### Training the model #####

print('\nTraining the model...\n')

X = df.tokenized_text
y = df.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

cv = CountVectorizer()
tfidf = TfidfTransformer()
model = SGDClassifier(learning_rate='optimal', 
                      loss='modified_huber', 
                      max_iter=10, 
                      random_state=42)

cv.fit(X_train)
tfidf.fit(cv.transform(X_train))

X_train = tfidf.transform(cv.transform(X_train))
X_test = tfidf.transform(cv.transform(X_test))

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f'The accuracy score is: {(y_pred == y_test).mean()}')

##### Output #####

with open('model.bin', 'wb') as f_out:
    pickle.dump((cv, tfidf, model), f_out)

print(f'\nThe model is saved to: "model.bin"')