#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 21:12:59 2017

@author: Sri
"""

import tweepy
import nltk
import TextBlob


def get_word_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)

    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

pos_tweets = [('I think the price will go up','positive'),
              ('I should buy bitcoins soon!','positive'),
              ('Prices are looking good','positive'),
              ('Looks promising','positive'),
              ('I am going to buy soon','positive'),
              ('I made a lot of money','positive'),
              ('Buy now!','positive'),
              ('I like where this is heading','positive'),
              ('The future looks promising','positive'),
              ('I love money','positive'),
              ('I am excited about the future','positive'),
              ('Invest now!','positive'),
              ('This is a reliable way to invest','positive'),
              ('I am confident','positive'),
              ('Bitcoin is great','positive'),
              ('Long now','positive')]
neg_tweets = [('Prices will go down soon','negative'),
              ('I am scared about bitcoins','negative'),
              ('Bitcoin is slowly dying','negative'),
              ('I am selling','negative'),
              ('Cryptocurrencies are unreliable','negative'),
              ('I lost a lot of money','negative'),
              ('Sell asap','negative'),
              ('Sell now','negative'),
              ('Prices will go down soon','negative'),
              ('I dont like where this is going','negative'),
              ('The future does not look promising','negative'),
              ('There is a coming cryptocurreny crash','negative'),
              ('Dont invest now','negative'),
              ('Prices are going to fall soon','negative'),
              ('I sense a price fall in the future','negative'),
              ('I am unsure','negative'),
              ('Bitcoin is terrible','negative'),
              ('Take your profits and run','negative'),
              ('There will be a dip soon','negative')]

tweets=[]
for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered,sentiment))


word_features = get_word_features(get_word_in_tweets(tweets))

training_set = nltk.classify.apply_features(extract_features,tweets)

classifier = nltk.NaiveBayesClassifier.train(training_set)

auth = tweepy.OAuthHandler('yW781OSTQWbW7ik5Z6pfEPTYo', 'YubyaE1EVsdy6DIEbrMCHyuFqZ2LNpllDQciHPCkLZDt7iEv7C')
auth.set_access_token('2944605422-c07iLPpdzzzx236JwPvJlI8lDTrIIBXZBbKWNfC', 'DQMNmc51auJ5vzQiWbDvfQd7lrJ48cHKRHBIV9L5r91hE')

api = tweepy.API(auth)

def get_min_id(public_tweets):
    ids = []
    for tweet in public_tweets:
        ids.append(tweet.id)
    if not ids:
        return 0
    else:
        return min(ids)

#searchQuery = 'BTC AND Bitcoin'

def get_tweets(hundred, sinceid, searchQuery):
    all_tweets = []
    for i in range(hundred):
        public_tweets = api.search(q = searchQuery,
                                   count = 100,
                                   since_id = sinceid,
                                   lang = 'en')
        for tweet in public_tweets:
            all_tweets.append(tweet.text)

        sinceid = get_min_id(public_tweets)

    return all_tweets, sinceid

def classify(tweets):

    total_score = 0.0

    positive = 0.0

    negative = 0.0
    
    for tweet in (tweets):
        sent = classifier.classify(extract_features(tweet.split()))
        if sent == 'positive':
            total_score = total_score + 1.0
            positive = positive + 1.0
        if sent == 'negative':
            total_score = total_score - 1.0
            negative = negative - 1.0

    return total_score, positive, negative, len(tweets)

#my_tweets = get_tweets(50)

#total_score,positive,negative, total = classify(my_tweets)

#historical_percent = (positive/total)
#historical_percent = historical_percent*100

#my_tweets_recent, sinceid = get_tweets(2,0)


#total_score1, positive1, negative1, total1 = classify(my_tweets_recent)
#current_percent = (positive1/total1)*100

#print total_score, positive, negative, total, historical_percent
#print total_score1, positive1, negative1, total1, current_percent

#if (current_percent > 1.022*historical_percent):
#    print "price will go up"
