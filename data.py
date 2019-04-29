#!/usr/bin/env python
import analyze

vocabulary = 10000
batch_size = 32
min_tweet_length =10
tweets_dir = 'tweets'


data = analyze.extract_all(output=None)
data, _ = analyze.divide_into_urdu_and_english(input=data, english_output=None, urdu_output=None)
data = analyze.sanitize(input=data, output=None)
#data = analyze.word_count(input=data, output=None,vocabulary=vocabulary, min_count=min_tweet_length)
#data = analyze.sort(input=data,  output=None)
analyze.create_data(input=list(data), min_tweet_length=min_tweet_length, vocabulary=vocabulary,output='{}/english_data_{}_{}.json'.format(tweets_dir, vocabulary, min_tweet_length))
