from collections.abc import Iterator
import glob, os
import itertools
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import  to_categorical
import numpy as np
import re
import json

class TweetSource:
    _delimiter = "!!!!!"
    def __init__(self, tweets, words, batch_size=2):
        self.tweets =tweets
        self.words = words
        self.num_words = len(self.words)+1
        self.batch_size = batch_size

    @property
    def tweet_count(self):
        return len(self.tweets)

    def _shuffle(self):
        current = 0
        count = 0
        indexes = []
        for tweet in self.tweets:
            l = len(tweet)
            if l != current:
                indexes.extend(np.random.permutation(count)+len(indexes))
                count = 0
                current = l
            count = count+1
        indexes.extend(np.random.permutation(count)+len(indexes))
        return indexes

    def generate_batches(self,):
        indexes = self._shuffle()
        tweet_index = 0
        while True:
            if tweet_index+self.batch_size >= self.tweet_count:
                tweet_index = 0
                indexes = self._shuffle()

            seqx=  [self.tweets[indexes[tweet_index+i]] for i in range(self.batch_size)]
           # print(batch_tweets)
            tweet_index += self.batch_size
            padx = pad_sequences(seqx)
            x = to_categorical(padx, num_classes=self.num_words)
            tail = np.full((self.batch_size, 1) , fill_value=0)
            pady = np.concatenate( (padx[:,1:], tail), axis=1)
            y = to_categorical(pady, num_classes=self.num_words)
            yield x,y

    def save_json(self, file):
        with open(file,"w") as f:
            f.write(json.dumps(self.words, indent=1))

if __name__ == "__main__":
    source = TweetSource('tweets/english_data_5000_10.json', batch_size=32)
    i = source.generate_batches()
    print(next(i))
    print(next(i))
    print(next(i))
    print(next(i))
    print(next(i))
