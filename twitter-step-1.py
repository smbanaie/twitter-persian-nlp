# -*- coding: utf-8 -*-import twitter_config

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import twitter_config
from datetime import datetime
import codecs
import pathlib

consumer_key = twitter_config.consumer_key
consumer_secret = twitter_config.consumer_secret
access_token = twitter_config.access_token
access_secret = twitter_config.access_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)



class TweetListener(StreamListener):
    counter = 0
    def on_data(self, data):
        try:
            self.counter +=1
            json_data = json.loads(data)
            # ایجاد پوشه و ذخیره توییت با آی دی در فایلهای متنی
            Tweet_Directory = 'tweets/'+datetime.now().strftime("%Y-%m-%d")
            pathlib.Path(Tweet_Directory).mkdir(parents=True, exist_ok=True)
            with codecs.open(Tweet_Directory+"/"+str(json_data["id"])+'.txt', 'a',encoding="utf-8") as f:
                f.write(json_data["id"],json_data["user"]["id"],json_data["timestamp"],json_data["text"],"|".join(json_data["entities"]["hashtags"]),json_data["text"].replace('\n', ' '))
                print("\n" + "*" * 50 + "\n" + str(self.counter) + " : \n" + json_data["text"].replace("\n", " "))
                return True






        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return False

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, TweetListener())
twitter_stream.filter(languages=['fa'], track=['با' , 'از','به','در'])
