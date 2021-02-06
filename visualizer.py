import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import re
import numpy as np

'''
This class is used to create all of the visuals in the application. It also categorizes all tweets into either positive
or negative (to be used for frequency). It provides 4 visuals: 
1. Sentiment_ratio = produces a bar plot that shows the frequency of positive and negative tweets
2. positive_common_words = produces a bar plot with the most frequent words in positive tweets. 
3. negative_common_words = produces a bar plot with the most frequent words in negative tweets.
4. keyword_search = produces all tweets that contain the designated keyword (keyword is obtained in the application 
    through get_keyword method.
'''

class Visualize:
    def __init__(self, data):
        self.data = data
        self.positive_tweets = [tweet for tweet in data[data['Sentiment'] == 'positive']
        ['Clean'] if isinstance(tweet, str)]
        self.negative_tweets = [tweet for tweet in data[data['Sentiment'] == 'negative']
        ['Clean'] if isinstance(tweet, str)]
        self.neutral_tweets = [tweet for tweet in data[data['Sentiment'] == 'neutral']
        ['Clean'] if isinstance(tweet, str)]

    def sentiment_ratio(self):
        values, counts = np.unique(self.data['Sentiment'],return_counts=True)
        fig = plt.figure(figsize=(8, 4))
        sns.barplot(x=values,
                    y=counts,
                    palette=sns.color_palette("muted"))
        plt.title('Tweet Count by sentiment')
        return fig

    def positive_common_words(self):
        # finding most common positive words
        pos_words = ' '.join(self.positive_tweets).split()
        pos_count = Counter(pos_words)
        pos_common_words = [word[0] for word in pos_count.most_common(20)]
        pos_common_counts = [word[1] for word in pos_count.most_common(20)]

        # plotting most common words using seaborn bar plot
        fig = plt.figure(figsize=(18, 6))
        ax = sns.barplot(x=pos_common_words, y=pos_common_counts, palette=sns.color_palette("muted"))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
        plt.title('Most common words in Positive Tweets')
        return fig

    def neutral_common_words(self):
        # finding most common negative words
        neut_words = ' '.join(self.neutral_tweets).split()
        neut_counts = Counter(neut_words)
        neut_common_words = [word[0] for word in neut_counts.most_common(20)]
        neut_common_counts = [word[1] for word in neut_counts.most_common(20)]

        # plotting most common words using seaborn bar plot
        fig = plt.figure(figsize=(18, 6))
        ax = sns.barplot(x=neut_common_words, y=neut_common_counts, palette=sns.color_palette("muted"))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
        plt.title('Most common words in Neutral Tweets')
        return fig


    def negative_common_words(self):
        # finding most common negative words
        neg_words = ' '.join(self.negative_tweets).split()
        neg_counts = Counter(neg_words)
        neg_common_words = [word[0] for word in neg_counts.most_common(20)]
        neg_common_counts = [word[1] for word in neg_counts.most_common(20)]

        # plotting most common words using seaborn bar plot
        fig = plt.figure(figsize=(18, 6))
        ax = sns.barplot(x=neg_common_words, y=neg_common_counts, palette=sns.color_palette("muted"))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
        plt.title('Most common words in Negative Tweets')
        return fig

    def get_keyword(self, keyword):
        self.keyword = re.compile(keyword, re.IGNORECASE)

    def keyword_search(self, text):
        if bool(self.keyword.search(text)):
            return text
