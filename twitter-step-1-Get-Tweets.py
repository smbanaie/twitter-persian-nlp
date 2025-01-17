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



class TweetListener(StreamListener):
    counter = 0
    def on_data(self, data):
        try:
            json_data = json.loads(data)
            Tweet_File_Name = 'tweets/'+datetime.now().strftime("%Y-%m-%d")+".txt"

            if 'extended_tweet' in json_data:
                if 'full_text' in json_data['extended_tweet']:
                    tweet_text = json_data['extended_tweet']['full_text']
                else:
                    tweet_text = json_data['text']
            elif 'text' in json_data:
                tweet_text = json_data['text']

            final_text = "%s\t%s\r\n" % (json_data["id"],(tweet_text.replace('\n', ' ')).replace('\t',''))

            if "RT" not in tweet_text:
                with codecs.open(Tweet_File_Name, 'a', encoding="utf-8") as f:
                    self.counter += 1
                    f.write(final_text)
                    print(str(self.counter) +"\t" + final_text)
            return True


        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return True

    def on_error(self, status):
        print(status)
        return True

try :

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth=auth,listener= TweetListener(),tweet_mode='extended')
    twitter_stream.filter(languages=['fa'], track=['با' , 'از','به','در'])

except Exception as e :
    print("Error Starting App : %s" % str(e))
