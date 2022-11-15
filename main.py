import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

import auth
import utils

# Setting column width to max
pd.set_option('display.max_colwidth', None)

# Input a query from the user & filter to remove retweets
query = input("Please enter a hashtag: ")
actual_tweets = query + "-filter:retweets"

# Generate the latest tweets on the given query
tweets = tweepy.Cursor(auth.api.search_tweets, q=actual_tweets, lang="en").items(20)

# Fetch the tweets and screen name and store it in a list
list1 = [[tweet.text, tweet.user.screen_name] for tweet in tweets]

# Convert the list into a dataframe
df = pd.DataFrame(data=list1, columns=['tweets', 'user'])

# Convert only the tweets into a list
tweet_list = df.tweets.to_list()

# Data cleaning
cleaned = [utils.clean_tweet(tw) for tw in tweet_list]

# Define the sentiment objects using TextBlob
sentiment_objects = [TextBlob(tweet) for tweet in cleaned]

# Create a list of polarity values and tweet text
sentiment_values = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_objects]

# Create a dataframe of each tweet against its polarity
sentiment_df = pd.DataFrame(sentiment_values, columns=["Polarity", "Tweet"])

print("Polarity data frame: \n", sentiment_df)

# Save the polarity column in a separate variable.
polarity_column = sentiment_df["Polarity"]

# Convert this column into a series.
polarity_series = pd.Series(polarity_column)

# Save the sentiments in a list
pos = 0
neg = 0
neu = 0
sentiment = []

# Create a loop to classify the tweets as Positive, Negative, or Neutral.
for items in polarity_series:
    if items > 0:
        pos = pos + 1
        sentiment.append("Positive")
    elif items < 0:
        neg = neg + 1
        sentiment.append("Negative")
    else:
        neu = neu + 1
        sentiment.append("Neutral")

# Add the sentiment list in our dataframe to see sentiment for every tweet.
sentiment_df['Polarity'] = sentiment
sentiment_df2 = sentiment_df.rename({'Polarity': 'Sentiment'}, axis=1)
print("Sentiment data frame: \n", sentiment_df2)


# Plot a pie chart
pieLabels = ["Positive", "Negative", "Neutral"]
populationShare = [pos, neg, neu]
figureObject, axesObject = plt.subplots()
axesObject.pie(populationShare, labels=pieLabels, autopct='%1.2f', startangle=90)
axesObject.axis('equal')
plt.show()

# Display the number of twitter users who feel a certain way about the given topic.
print("%f percent of twitter users feel positive about %s"%(pos, query))
print("%f percent of twitter users feel negative about %s"%(neg, query))
print("%f percent of twitter users feel neutral about %s"%(neu, query))

# Create a Wordcloud from the tweets
all_words = ' '.join([text for text in cleaned])
wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()
