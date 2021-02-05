import pandas as pd
from text_cleaner import Text_cleaner

data = pd.read_csv("Data\data_1.csv", encoding="latin-1")

# data columns were accidentally set to a tweet, this corrects them:
data.columns = ['Sentiment', 'id', 'Date', 'Query', 'User', 'Tweet']

# this removes unneeded data and columns:
data = data.drop(columns=['id', 'Date', 'Query', 'User'], axis=1)

# this dictionary will be used to decode sentiment values from opaque number to a more clear categorical label
f = {0: 'Negative', 4: 'Positive'}


# this section applies the dictionary to the data using a lambda function:
def sentiment_decoder(sentiment):
    return f[sentiment]


data.Sentiment = data.Sentiment.apply(lambda x: sentiment_decoder(x))
text_cleaner = Text_cleaner()
data.Tweet = data.Tweet.apply(lambda x: text_cleaner.clean(x))

# this creates the new processed data:
data.to_csv(r'Processed\cleaned_data.csv')
