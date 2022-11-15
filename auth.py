import tweepy

# Authentication
consumer_key = "lPG5nsVL1MLfPOXQYjiZWmMDy"
consumer_secret = "BpD8OIY6bpY8BHnZdZq2UGedQ3HhNXUwX9kCvDhxt9cnTie93r"
access_token = "388728828-eda22V9DbIiuk5XjXJ5gQrMVCXdNWTytYn3NvEMV"
access_token_secret = "yTDb86ev1el1igWOGyz76wHamTWna0LsZAB9vVsVzeQbK"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
