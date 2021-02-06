import tweepy

'''
This is class to access the Twitter API using the appropriate credentials. Once the credentials are set, a method called 
set_api accesses the API and sets a new attribute for the tweet class can access it. 
'''

class User:

    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret
        self.api = None

    # grants access to the twitter api by using the various keys, sets the attribute api for the tweet class to use
    def set_api(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret, callback_url)
        auth.set_access_token(self.access_token, self.access_secret)
        self.api = tweepy.API(auth)
        
