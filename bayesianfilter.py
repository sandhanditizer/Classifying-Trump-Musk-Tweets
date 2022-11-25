"""
Zachariah Kline
May 2, 2022
Classifying the difference between Donald Trump tweets and Elon Musk tweets.
"""

import re
import math
from scrub_tweets import collect_musk_tweets, collect_trump_tweets
from read_write_database import read_database, write_database

# Threasholds
MAX_MUSK_SCORE = 0.45
MIN_TRUMP_SCORE = 0.55

def trump_probability(feature):
    trump_count = feature['trump_count']
    musk_count = feature['musk_count']
    
    trump_frequency = trump_count / max(1, database['total_trumps'])
    musk_frequency = musk_count / max(1, database['total_musks'])
    
    return trump_frequency / (trump_frequency + musk_frequency)

def bayesian_probability(feature, assumed_prob=0.5, weight=1):
    basic_probability = trump_probability(feature)
    data_points = feature['trump_count'] + feature['musk_count']
    numerator = weight * assumed_prob + data_points * basic_probability
    denominator = weight + data_points
    new_probability = numerator / denominator
    
    return new_probability

def inverse_chi_squared(value, degrees_of_freedom):
    if degrees_of_freedom % 2 != 0:
        raise ValueError('degrees_of_freedom must be even')
    m = value / 2
    sum = term = math.exp(-m)
    for i in range(1, degrees_of_freedom // 2):
        term *= m / i
        sum += term
    return min(sum, 1.0)

def fisher(probabilities, num_prob):
    value = -2 * sum(map(math.log, probabilities))
    dof = 2  * num_prob
    return inverse_chi_squared(value, dof)

def untrained(feature):
    return feature['trump_count'] == 0 and feature['musk_count'] == 0

def score(features):
    trump_prob = []
    musk_prob = []
    num_prob = 0
    for feature in features:
        if untrained(feature):
            # Skip features that dont appear in training
            continue
        
        t_probability = bayesian_probability(feature)
        trump_prob.append(t_probability)
        
        musk_prob.append(1 - t_probability)
    
    m = 1 - fisher(trump_prob, num_prob)
    p = 1 - fisher(musk_prob, num_prob)
    return (1 - m + p) / 2

def classification(score):
    if score <= MAX_MUSK_SCORE:
        return 'Musk'
    elif score >= MIN_TRUMP_SCORE:
        return 'Trump'
    else:
        return 'unsure'

def create_word_feature(word, trump_count = 0, musk_count = 0):
    return {'word': word, 'trump_count': trump_count, 'musk_count': musk_count}

def intern_feature(word):
    if word in database['features']:
        return database['features'][word]
    else:
        feature = create_word_feature(word)
        database['features'][word] = feature
        return feature
        
def extract_words(text):
    pattern = re.compile('[a-zA-Z]{6,}') #I increased the word size since I got better results
    words = pattern.findall(text)        # with 6 instead of 3
    return set(words)

def extract_features(text):
    words = extract_words(text)
    return [intern_feature(word) for word in words]

def classify(text):
    features = extract_features(text)
    value = score(features) #Between 0 and 1
    who = classification(value)
    
    #I force it to have a 'hunch' on who the tweet belongs to
    if who == 'unsure' and MAX_MUSK_SCORE < value < 0.5:
        msg = "I'm not too sure who this tweet came from. However I'm leaning more towards Elon Musk."
    elif who == 'unsure' and MIN_TRUMP_SCORE > value > 0.5:
        msg = "I'm not too sure who this tweet came from. However I'm leaning more towards Donald Trump."
    else:
        if who == 'Musk':
            value = 1 - value
            
        msg = f'This tweet is from {who} | {round(value, 3) * 100}% Certainty'
        
    return msg
    
def increment_count(feature, type):
    if type == 'Musk':
        feature['musk_count'] += 1
    elif type == 'Trump':
        feature['trump_count'] += 1
    else:
        raise TypeError(f'Expected musk or trump, received {type}')
    
def increment_total_count(type):
    if type == 'Musk':
        database['total_musks'] += 1
    else:
        database['total_trumps'] += 1
        
def train(text, type):
    for feature in extract_features(text):
        increment_count(feature, type)
        
    return increment_total_count(type)

    

#---------------------------------------------------------

if __name__ == '__main__':
    database = read_database('database.pkl') # Get the database which I previously trained
    for tweet in collect_musk_tweets('Musk_Dataset/'):
        train(tweet, 'Musk')
    print('Musk training complete.')
        
    for tweet in collect_trump_tweets('Trump_Dataset/'):
        train(tweet, 'Trump')
    print('Trump training complete.')
    
    write_database(database, 'trained_database.pkl') # Demoed to show it works
    
    # Now you can try the tweets I provided in the README file
    # classify('Republicans and Democrats have both created our economic problems.')
    # classify('Next I’m buying Coca-Cola to put the cocaine back in')