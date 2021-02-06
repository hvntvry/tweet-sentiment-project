from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
import streamlit as st
import numpy as np

'''
This class is the machine learning model. It is not used in the main application, it is used in model.py to train, test
and then pickle the model. The advantage of this is that the application will work faster with a prepared model.
Furthermore, partial fit can be used on the pickled model. The original Classifier is naive baye's. The inherited model
is a SGD classifier, which has the additional method partial_fit for online-learning. 
'''

class Classifier:
    def __init__(self, text, sentiment):
        self.text = text
        self.sentiment = sentiment
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()
        self.prepared_text = None
        self.model = None

    # this method fits and transforms the vectors and trains the model
    def prepare_model(self):
        self.prepared_text = self.vectorizer.fit_transform(self.text.values.astype('U'))
        self.model = self.classifier.fit(self.prepared_text, self.sentiment)

    # this method takes the column of a dataframe and returns an array with the predictions to add to the dataframe
    def classify(self, tweet):
        prepared_tweet = self.vectorizer.transform(tweet)
        prediction = self.model.predict(prepared_tweet)
        prediction_array = np.array(prediction)
        return prediction_array


class Linear(Classifier):
    def __init__(self, text, sentiment):
        super().__init__(text, sentiment)
        self.classifier = SGDClassifier(loss='hinge', penalty='l2', alpha=0.001, random_state=42, max_iter=100, tol=None)

    def partial_fit(self, x, y):
        x = self.vectorizer.transform(x)
        self.model.partial_fit(x, y)
