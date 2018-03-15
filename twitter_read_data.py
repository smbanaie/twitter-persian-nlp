# -*- coding: utf-8 -*-import twitter_config

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import twitter_config
from langdetect import detect
from datetime import datetime
import time





consumer_key = twitter_config.consumer_key
consumer_secret = twitter_config.consumer_secret
access_token = twitter_config.access_token
access_secret = twitter_config.access_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# api = tweepy.API(auth)

# Using the API object to get tweets from your timeline, and storing it in a variable called public_tweets



class TweetListener(StreamListener):
    # def __init__(self):
        # self.client = pykafka.KafkaClient("localhost:9092")
        # self.producer = self.client.topics[bytes('twitter','utf-8')].get_producer()

    def on_data(self, data):
        try:
            # print(""+data)
            with open('tweets.json', 'a') as f:
                f.write(data)
            json_data = json.loads(data)
            print(json_data["id"])
            print(json_data["user"]["id"])
            print(json_data["text"])
            print(json_data["created_at"])
            print(json_data["retweet_count"])
            print(json_data["favorite_count"])
            print(json_data["user"]["followers_count"])
            print("-"*20)
            info = {}


            info["id"] =json_data["id"]
            info["text"] =json_data["text"]
            info["created_at"] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(json_data["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
            # ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(json_data["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
            info["retweet_count"] =json_data["retweet_count"]
            info["favorite_count"] =json_data["favorite_count"]
            info["followers_count"] =json_data["user"]["followers_count"]
            # info["hashtags"] =json_data["entities"]["hashtags"]
            info["user_id"] =json_data["user"]["id"]
            info["hashtags"] = []
            if len(json_data["entities"]["hashtags"]) > 0:
                for hashtag in json_data["entities"]["hashtags"]:
                    try:
                        lng = detect(hashtag["text"])
                        if lng == "fa" or lng == "ar" or lng == "ur":
                            print("Tag : " + hashtag["text"] + " --- Lang : " + lng)
                            info["hashtags"].append(hashtag)
                    except:
                        pass
            print("-" * 20)
            # words = json_data['text'].split()
            #
            # ls = list(filter(lambda x: x.lower().startswith('#'), words))
            # if(len(ls)!=0):
            # 	print(json_data['text'])
            # 	for word in ls:
            # 		print(word[1:])
            # 		# self.producer.produce(bytes(word,'utf-8'))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return False

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, TweetListener())
twitter_stream.filter(languages=['fa'], track=['با'  ])
