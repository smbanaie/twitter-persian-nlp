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
            json_data = json.loads(data)
            # ایجاد پوشه و ذخیره توییت با آی دی در فایلهای متنی
            Tweet_Directory = 'tweets/'+datetime.now().strftime("%Y-%m-%d")

            if 'extended_tweet' in json_data:
                if 'full_text' in json_data['extended_tweet']:
                    tweet_text = json_data['extended_tweet']['full_text']
                else:
                    pass  # i need to figure out what is possible here
            elif 'text' in json_data:
                tweet_text = json_data['text']

            tweet_text = tweet_text.replace('\n', ' ').replace("\t"," ")
            if "RT" not in tweet_text :
                with codecs.open("tweets-hashtags/" + datetime.now().strftime("%Y-%m-%d") + '.txt', 'a',
                                 encoding="utf-8") as f:
                    self.counter += 1
                    str_out = json_data["id_str"] + "\t"
                    tags = ""
                    for hashtag in json_data["entities"]["hashtags"]:
                        tags = tags + "," + hashtag["text"]
                    if tags != "":
                        tags = tags[1:]
                    str_out = str_out + "\t" + tags + "\t" + tweet_text + "\r\n"
                    f.write(str_out)
                    print(str(self.counter) + " : \t" + str_out)
            return True


        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, TweetListener())
twitter_stream.filter(languages=['fa'], track=['با' , 'از','به','در'])
