"""
Zachariah Kline
May 2, 2022
Functions that scrape tweets from csv files.
"""

import os
import csv
import re

def remove_URL(text):
    """Remove URLs from text."""
    return re.sub(r'http\S+', '', text)
    
def remove_emoji(text):
    """Removes any emojis from text."""
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  #Emoticons
        u"\U0001F300-\U0001F5FF"  #Symbols & pictographs
        u"\U0001F680-\U0001F6FF"  #Transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  #Flags (iOS)
        u"\U00002500-\U00002BEF"  #Chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  #Dingbats
        u"\u3030"
        "]+", re.UNICODE)
    return re.sub(emoj, '', text)

def extract_musk(filename):
    """Parses through a given csv file to extract all the tweets specific to Elon Musk"""
    all_tweets = [] #All tweets per file
    with open(filename, mode='r') as file:
        dict_readable = csv.DictReader(file) #Create dictionary of all the data in file
        for row in dict_readable:
            tweet = row['tweet'] #We only care about the row of tweets
            tweet = remove_emoji(tweet) #Useless data
            tweet = remove_URL(tweet) #Useless data
            all_tweets.append(tweet)
        
    return all_tweets
    
def extract_trump(filename):
    """Parses through a csv file to extract all the tweets specific to Donald Trump"""
    all_tweets = []
    with open(filename, mode='r') as file:
        dict_readable = csv.DictReader(file)
        count = 0
        for row in dict_readable:
            if count < 10: #Skip the first 10 rows for testing
                count += 1
                continue
            else:
                tweet = row['text']
                tweet = remove_emoji(tweet)
                tweet = remove_URL(tweet)
                if tweet.startswith('RT :'): #Removes retweets
                    continue
                else:
                    all_tweets.append(tweet)
                
                count += 1
        
    return all_tweets

def collect_musk_tweets(folder):
    """
    Collects all tweets (in csv format) from a given folder.\n

    Returns:\n
        list: All Trump tweets.
    """
    files = os.listdir(folder)
    tweets = []
    tweet_count = 0
    for fn in files:
        if fn == '.DS_Store': #Skip over since it is not needed
            continue
        
        #All tweets in one csv file
        all_tweets = extract_musk(os.path.join(folder, fn))
        
        for tweet in all_tweets: #Puts every tweet in one list for convenience
            tweets.append(tweet)
            tweet_count += 1
    
    print(f'{tweet_count} Musk tweets were collected from {len(files) - 1} file(s).')
    return tweets

def collect_trump_tweets(folder):
    """
    Collects all tweets (in csv format) from a given folder.\n

    Returns:\n
        list: All Musk tweets.
    """
    files = os.listdir(folder)
    tweets = []
    tweet_count = 0
    for fn in files:
        if fn == '.DS_Store':
            continue
        
        all_tweets = extract_trump(os.path.join(folder, fn))
        
        for tweet in all_tweets:
            tweets.append(tweet)
            tweet_count += 1
            
    print(f'{tweet_count} Trump tweets were collected from {len(files) - 1} file(s).')
    return tweets