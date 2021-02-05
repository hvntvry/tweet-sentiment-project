from sklearn.model_selection import train_test_split
import numpy as np
import pickle
import pandas as pd
from prediction import Classifier, Linear
from sklearn import metrics

'''
Training and pickling of the current model I chose, a SGDclassifier or stochastic gradient descent from sklearn. (see
the prediction class for more information). In a comparison between Multinomial (Naive Baye's) classifier, support 
vector classifier and the SGD, all achieved around 70-80% accuracy. The advantage of the SGDclassifier is the ability to 
partial_fit, which I leveraged to allow for online-learning. Hopefully, The model will improve with user feedback, 
surpassing the 75-80% accuracy.  
'''

data = pd.read_csv('Processed\cleaned_data.csv', encoding="latin-1") # check data explore file for more info

X_train, X_test, y_train, y_test = train_test_split(data.Tweet, data.Sentiment, test_size=0.33, random_state=42)

model = Linear(X_train, y_train)

model.prepare_model()

predicted = model.classify(X_test)

print(np.mean(predicted == y_test))

print(metrics.classification_report(y_test, predicted))

pickle.dump(model, open('model_clf.pkl', 'wb'))
