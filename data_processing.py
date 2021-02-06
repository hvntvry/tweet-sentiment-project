import pandas as pd
from text_cleaner import Text_cleaner

'''
main data found here: https://www.kaggle.com/arkhoshghalb/twitter-sentiment-analysis-hatred-speech.
I have selected this data because it is light-weight and distinguishes between 
positive, neutral and negative. There was some missing data that is dropped 
below. The data is slightly imbalanced, so I have used another data set to
boost the positive and negative tweets. 
'''

data = pd.read_csv("Data\\tweet_dataset.csv", encoding="latin-1")
data = data.drop(columns=['textID', 'sentiment', 'author', 'old_text', 'aux_id', 'selected_text'], axis=1)
data = data.dropna()
data.columns = ['Tweet', 'Sentiment']
#text_cleaner = Text_cleaner()
#data.Tweet = data.Tweet.apply(lambda x: text_cleaner.clean_tweet_elements(x))
data = data.dropna()
data.to_csv(r'Processed\cleaned_data.csv')


'''
I have decided to partial train the model on some more data, from this very 
large dataset with binary positive and negative tweets. I did this due to the
imbalance in the previous data, Neutral has 12,602, Positive has 9897, Negative
has 8,830. I found the model tended to predict neutral, and wanted to balance
the prediction. 
'''
#this data can be downloaded at https://www.kaggle.com/kazanova/sentiment140
data_boost = pd.read_csv("Data\data_1.csv", encoding="latin-1")

# data columns were accidentally set to a tweet, this corrects them:
data_boost.columns = ['Sentiment', 'id', 'Date', 'Query', 'User', 'Tweet']

# this removes unneeded data and columns:
data_boost = data_boost.drop(columns=['id', 'Date', 'Query', 'User'], axis=1)

#taking heads and tails of data, to ensure equal positive and negative represenation.
data_head = data_boost.head(3000)
data_tail = data_boost.tail(2000)
data_boost = pd.concat([data_head, data_tail], axis=0)

# this dictionary will be used to decode sentiment values from opaque number to a more clear categorical label
f = {0: 'negative', 4: 'positive'}


# this section applies the dictionary to the data using a lambda function:
def sentiment_decoder(sentiment):
    return f[sentiment]


data_boost.Sentiment = data_boost.Sentiment.apply(lambda x: sentiment_decoder(x))
#text_cleaner = Text_cleaner()
#data_boost.Tweet = data_boost.Tweet.apply(lambda x: text_cleaner.clean_tweet_elements(x))

# this creates the new processed data:
data_boost.to_csv(r'Processed\data_boost.csv')