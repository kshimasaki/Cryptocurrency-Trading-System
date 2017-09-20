#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 21:12:59 2017

@author: Sri
"""

import tweepy
import nltk


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
              ('Long now','positive'),
              ('This will recover soon','positive'),
              ('Has increased price','positive'),
              ('BTC looking bullish','positive'),
              ('This is looking bullish','positive'),
              ('Reasons to be excited','positive'),
              ('Surpasses $4000','positive'),
              ('It is beautiful','positive'),
              ('Ethereum will rise soon','positive'),
              ('ETH looking good','positive'),
              ('ETH looking bullish','positive'),
              ('Good things are coming','positive'),
              ('This is looking like a good investment','positive'),
              ('We are going towards the moon','positive'),
              ('Congratulations!','positive'),
              ('Prices are supposed to rise soon','positive'),
              ('This is a great use','positive'),
              ('ETH is a buy','negative')]
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
              ('There will be a dip soon','negative'),
              ('This wont recover soon','negative'),
              ('Has decreased price','negative'),
              ('bearish','negative'),
              ('This is looking bearish','negative'),
              ('I am going to short','negative'),
              ('We are in a bubble','negative'),
              ('Ethereum is falling','negative'),
              ('Steep fall soon','negative'),
              ('This is a bad investment','negative'),
              ('This is going down','negative'),
              ('These fees are way to high','negative'),
              ('No conformation','negative'),
              ('This has been stuck','negative'),
              ('We will dip soon','negative'),
              ('Short dip before we break the barrier','negative'),
              ('Dont buy','negative')]

tweets=[]
for (words, sentiment) in (pos_tweets + neg_tweets):
    words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
    tweets.append((words_filtered,sentiment))


word_features = get_word_features(get_word_in_tweets(tweets))

training_set = nltk.classify.apply_features(extract_features,tweets)

classifier = nltk.NaiveBayesClassifier.train(training_set)

auth = tweepy.OAuthHandler('', '')
auth.set_access_token('', '')

api = tweepy.API(auth, wait_on_rate_limit = True)

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
        public_tweets1 = api.search(q = searchQuery,
                                   count = 100,
                                   since_id = sinceid,
                                   lang = 'en')
        sinceid = get_min_id(public_tweets1)

        for tweet in (public_tweets1):
            all_tweets.append(tweet.text)

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
            negative = negative + 1.0

    total = positive + negative
    return total_score, positive, negative, total
