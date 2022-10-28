import tweepy

# Authentication
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Access Twitter Data
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)