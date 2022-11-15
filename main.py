import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

import auth
import utils

# Input a query from the user & filter to remove retweets
query = input("Please enter a hashtag: ")
actual_tweets = query + "-filter:retweets"

# Generate the latest tweets on the given query
tweets = tweepy.Cursor(auth.api.search_tweets, q=actual_tweets, lang="en").items(100)

# Create a list of the tweets, the users, and their location
list1 = [[tweet.text, tweet.user.screen_name, tweet.user.location] for tweet in tweets]

# Convert the list into a dataframe
df = pd.DataFrame(data=list1, columns=['tweets', 'user', "location"])

# Convert only the tweets into a list
tweet_list = df.tweets.to_list()

# Data cleaning
cleaned = [utils.clean_tweet(tw) for tw in tweet_list]
print("List of tweet", cleaned)
print("Number of tweet", len(cleaned))

# Define the sentiment objects using TextBlob
sentiment_objects = [TextBlob(tweet) for tweet in cleaned]
print("Sentiment objects: ", sentiment_objects[0].polarity, sentiment_objects[0])

# Create a list of polarity values and tweet text
sentiment_values = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_objects]
# Print the value of the 0th row.
print("Sentiment values: ", sentiment_values[0])

# Print all the sentiment values
print("All sentiment values: ", sentiment_values[0:99])

# Create a dataframe of each tweet against its polarity
sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])
print("Sentiment data frame: \n", sentiment_df)

# Save the polarity column as 'n'.
n = sentiment_df["polarity"]

# Convert this column into a series, 'm'.
m = pd.Series(n)
print(m)

# Initialize variables, 'pos', 'neg', 'neu'.
pos = 0
neg = 0
neu = 0

# Create a loop to classify the tweets as Positive, Negative, or Neutral.
# Count the number of each.
for items in m:
    if items > 0:
        print("Positive")
        pos = pos + 1
    elif items < 0:
        print("Negative")
        neg = neg + 1
    else:
        print("Neutral")
        neu = neu + 1

print("Positive:", pos, "Negative:", neg, "Neutral:", neu)

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
