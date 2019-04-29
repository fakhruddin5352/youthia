import glob
import json
import re
from collections.abc import  Iterator, Iterable
from keras.preprocessing.text import Tokenizer

class Record:
    pass

def write_output(output, data, do_unique=True, do_list=True):
    if output:
        with open(output,"w") as outfile:
            if do_unique and not isinstance(data, set) and (isinstance(data, Iterator) or isinstance(data, Iterable)):
                data = set(data)
            if do_list and not isinstance(data, list) and (isinstance(data, Iterator) or isinstance(data, Iterable)):
                data = list(data)
            outfile.write(json.dumps(data, indent=1))
    return data

def load_input(input):
    if isinstance(input, str):
        with open(input, "r") as file:
            tweet = json.loads(' '.join(file.readlines()))
            return tweet
    return input

def extract_text_from_tweet(path):
    tweet = load_input(path)
    return tweet['text']

def extract_all(input="data/**/*.json", output="tweets/all.json", max_tweets=99999999999):
    paths = set(glob.glob(input))
    tweets = (extract_text_from_tweet(path) for path,_ in zip(paths,range(max_tweets)))
    return write_output(output, tweets)

def has_urdu_chars(tweet):
    return \
    any(char for char in tweet if char >= chr(0x600) and char <= chr(0x6FF) )  or \
    any(char for char in tweet if char >= chr(0xFB50) and char <= chr(0xFDFF)) or \
    any(char for char in tweet if char >= chr(0xFE70) and char <= chr(0xFEFF))

def divide_into_urdu_and_english(input="tweets/all.json", english_output="tweets/english.json", urdu_output="tweets/urdu.json"):
    tweets = load_input(input)
    urdu = (tweet for tweet in tweets if has_urdu_chars(tweet))
    english = (tweet for tweet in tweets if not has_urdu_chars(tweet))
    return write_output(english_output, (english)), write_output(urdu_output, (urdu))

def replace_url(tweet):
    return re.sub('https?:\/\/(?:[-\w.]\/?)+', '', tweet)

def sanitize(input='tweets/english.json',output='tweets/english_sanitized.json'):
    tweets = load_input(input)
    tweets =  (replace_url(tweet) for tweet in tweets)
    tweets = (tweet.replace("..",".") for tweet in tweets)
    tweets = (tweet.replace(",," ,",") for tweet in tweets)
    tweets = (tweet.replace("!!","!") for tweet in tweets)
    tweets = (tweet.replace("??","?") for tweet in tweets)

    tweets = (tweet.replace("."," .") for tweet in tweets)
    tweets = (tweet.replace("," ," ,") for tweet in tweets)
    tweets = (tweet.replace("!"," !") for tweet in tweets)
    tweets = (tweet.replace("?"," ?") for tweet in tweets)
    tweets = (tweet for tweet in tweets if tweet.strip())
    return write_output(output,tweets)

def word_count(input='tweets/english_sanitized.json', output='tweets/english_word_count.json', vocabulary=None, min_count = 1):
    tweets = set(load_input(input))
    tokenizer = Tokenizer(filters='"(*+/;<=>[\\]^_`{|}~\t\n', num_words=vocabulary)
    tokenizer.fit_on_texts(tweets)
    word_counts = {tweet: len(tokenizer.texts_to_sequences([tweet])[0]) for tweet in tweets }
    remove_zeros = {tweet : word_counts[tweet] for tweet in word_counts if word_counts[tweet] >= min_count}
    return write_output(output, remove_zeros, do_unique=False, do_list=False)

def histogram(input='tweets/english_word_count.json', output='tweets/english_histogram.json'):
    tweets = load_input(input)
    hist = dict()
    for count in tweets.values():
        try:
            hist[count] += 1
        except KeyError:
            hist[count] = 1
    return write_output(output, hist, do_unique=False, do_list=False)

def sort(input='tweets/english_word_count.json', output='tweets/english_sorted.json'):
    tweets = load_input(input)
    data = sorted(tweets, key= lambda  tweet: tweets[tweet])
    return write_output(output, data, do_unique=False, do_list=True)

def create_data(input='tweets/english_sorted.json', output='tweets/english_data.json', vocabulary=999999999, min_tweet_length=0):
    tweets = load_input(input)
    tokenizer = Tokenizer(filters='"(*+/;<=>[\\]^_`{|}~\t\n', num_words=vocabulary)
    tokenizer.fit_on_texts(tweets)
    data = dict()
    seq = tokenizer.texts_to_sequences(tweets)
    seq = [tweet for tweet in seq if len(tweet)>=min_tweet_length]
    seq = sorted(seq, key=lambda  tweet: len(tweet))
    data['tweets'] = seq
    words = tokenizer.word_index
    data['words'] = [word for word,_ in zip(words, range(vocabulary))]
    data['count'] = len(seq)
    data['word_count'] = len(data['words'])
    return write_output(output, data, do_unique=False, do_list=False)

def stats(input='tweets/english_sanitized.json', output='tweets/stats.json'):
    tweets = load_input(input)
    tokenizer = Tokenizer(filters='"(*+/;<=>[\\]^_`{|}~\t\n')
    tokenizer.fit_on_texts(tweets)

    data = dict()
    data['count'] = len(tweets)
    data['unique_words'] = len(tokenizer.word_index)
    data['word_counts'] = tokenizer.word_counts
    return write_output(output, data, do_unique=False, do_list=False)
