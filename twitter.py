from TwitterSearch import *
import itertools
import json
import os
import re
import time

def is_user_pti(search):
    tso = TwitterUserOrder(search)  # create a TwitterSearchOrder object
    tso.set_exclude_replies(exclude=True)
    tso.set_include_entities(False)
    tso.set_include_rts(False)
    tso.set_count(1)


    ts = TwitterSearch(
        consumer_key='M3U9e4qd0fVQsXGwrYgUV7DDw',
        consumer_secret='zDKAEkafkyDXc2aR9B52yUMXQVRWQnh61k3lPnBH2D19dRuFNb',
        access_token='878658300-lIihymc7i3xCzZaVGIGhbql5C1IvSf4S7BvkASi0',
        access_token_secret='fkeBUt8oSJpaIbyYkUyfru1paQuh2frA8rWQH69xoOcUg'
    )
    for (c, tweet) in zip(itertools.count(), ts.search_tweets_iterable(tso)):
        return re.search('PTI', tweet['user']['description'])

    return False

def source_user(search):
    try:
        tso = TwitterUserOrder(search) # create a TwitterSearchOrder object
        tso.set_exclude_replies(exclude=True)
       # tso = TwitterSearchOrder()
       # tso.set_keywords([search])
    #    tso.set_since(datetime.date(2018,1,1))
        tso.set_include_entities(False)
        tso.set_include_rts(False)
        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key = 'M3U9e4qd0fVQsXGwrYgUV7DDw',
            consumer_secret = 'zDKAEkafkyDXc2aR9B52yUMXQVRWQnh61k3lPnBH2D19dRuFNb',
            access_token = '878658300-lIihymc7i3xCzZaVGIGhbql5C1IvSf4S7BvkASi0',
            access_token_secret = 'fkeBUt8oSJpaIbyYkUyfru1paQuh2frA8rWQH69xoOcUg'
         )

        references = set()

         # this is where the fun actually starts :)
        tweet_dir = "data/{}".format(search)
        if not os.path.isdir(tweet_dir):
            os.mkdir(tweet_dir)

        source_count = 0
        for (c,tweet) in zip(itertools.count() ,ts.search_tweets_iterable(tso)):
            references.update(re.findall("@\w+", tweet['text']))
            tweet_path = "{}/{}.json".format(tweet_dir, tweet['id_str'])
            if os.path.isfile(tweet_path):
                continue
            with open(tweet_path, "w") as file:
                file.write(json.dumps(tweet))
                source_count += 1

        print("{} tweets sourced from {}".format(source_count, search))

        for reference in references:

            username = reference[1:]
            userdir = "data/{}".format(username)
            if not os.path.isdir(userdir):
                os.mkdir(userdir)
                time.sleep(20)
                try:
                    if is_user_pti(username):
                        print('Sourcing user {}'.format(username))
                        source_user(username)
                except TwitterSearchException as e: # take care of all those ugly errors if there are some
                    print(e)


    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)

if __name__ == "__main__":
    source_user("SajjadFayazKhan")