import tweepy
import pandas as pd

'''
This class is used to access twitter, using the API, and scrape the replies to a tweet using the method reply_scrape.
'''
        
class Tweet:
    def __init__(self, username, tweet_id, user_api, tweet_amount):
        self.username = username
        self.tweet_id = tweet_id
        self.user_api = user_api
        self.tweet_amount = tweet_amount
        self.replies_data = None

    # access twitter api to get all the replies from one tweet, then returns a data frame of the replies w/ usernames
    def reply_scrape(self):
        replies_name = {}
        replies_text = {}
        count = 0
        for tweet in tweepy.Cursor(self.user_api.search, q='to:' + self.username, result_type='recent',
                                   timeout=999999).items(
            self.tweet_amount):
            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if len(self.tweet_id) > 5:
                    if (tweet.in_reply_to_status_id_str == self.tweet_id):
                        replies_name[count] = tweet.user.screen_name
                        replies_text[count] = tweet.text
                else:
                    replies_name[count] = tweet.user.screen_name
                    replies_text[count] = tweet.text
            count += 1
        self.replies_data = pd.DataFrame({'User': replies_name, 'Text': replies_text})



