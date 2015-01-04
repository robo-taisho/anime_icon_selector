#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import codecs
import tweet_parser
import username
import os
from gensim import corpora

### Constants
MECAB_MODE = 'mecabrc'
PARSE_TEXT_ENCODING = 'utf-8'



moziretu = ""


def get_tweets_from_csv(filename):
    ret = csv.reader(open(filename))
    tweets = [r[0].decode('utf-8') for r in ret]
    
    for tweet in tweets[:]:
        if len(tweet) <= 3:
            tweets.remove(tweet)
    return tweets

def main(user_name):
    FILENAME = user_name + ".csv"
    sample_u = get_tweets_from_csv(FILENAME)
    mozi = unite(sample_u)
    words_dict = tweet_parser.parse(mozi)
    wordlist = wordslist(words_dict)
    return wordlist


def wordslist(words_dict):
    words = ",".join(words_dict['nouns']).encode("utf-8")
    wordlist = []
    wordlist = words.split(",")
    return wordlist

def unite(sample_u):
    moziretu = ""
    for i in range(1,len(sample_u)):
        moziretu = moziretu + sample_u[i]
    return moziretu


def filter_dictionary(dictionary):
    '''
        低頻度と高頻度のワードを除く感じで
        '''
    dictionary.filter_extremes(no_below=2, no_above=0.5)  # この数字はあとで変えるかも
    return dictionary

    #dictionary.filter_extremes(no_below=2, no_above=0.5)


if __name__ == '__main__':
    arr = []
    os.chdir('usertweet')
    user_name = username.user_name
    
    for i in range(0,len(user_name)):
        
        arr.append(main(user_name[i]))
        """
        sample_u = get_tweets_from_csv(FILENAME)
        print len(sample_u)
        mozi = unite(sample_u)
        words_dict = tweet_parser.parse(mozi)
        wordlist = wordslist(words_dict)
        arr.append(wordlist)
        """
    
    dictionary = filter_dictionary(corpora.Dictionary(arr))
    #print(dictionary.token2id)
    os.chdir('../.')
    dictionary.save_as_text('twitdic.txt')

    for k,v in dictionary.iteritems():
        print k,v

