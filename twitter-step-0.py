# -*- coding: utf-8 -*-import twitter_config

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import twitter_config
from datetime import datetime
import codecs



consumer_key = twitter_config.consumer_key
consumer_secret = twitter_config.consumer_secret
access_token = twitter_config.access_token
access_secret = twitter_config.access_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)



class TweetListener(StreamListener):

    def on_data(self, data):

            json_data = json.loads(data)
            print("Original Data : ")

            print("Tweet ID : "+str(json_data["id"]))
            print(" User ID : "+str(json_data["user"]["id"]))
            print(" User Name : " + json_data["user"]["name"])
            print(" Tweet Text :"+json_data["text"])
            print(" Tweet Date :"+json_data["created_at"])
            # برای نمایش و چاپ اطلاعات یوزر باید آنها را به رشته تبدیل کنیم، تابد دامپ این کار را برای ما انجام میدهد
            print("User Info : \n" +json.dumps(json_data["user"]))
            print("-" * 20)
            print("Original Data : ")
            print(data)
            print("-" * 20)

            return True


    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, TweetListener())
twitter_stream.filter(languages=['fa'], track=['با' , 'از','به','در'])
