# -*- coding: utf-8 -*-import twitter_config
import os,fnmatch,codecs
import re



counter = 0
for dirpath, dirs, files in os.walk('tweets'):
	for filename in fnmatch.filter(files, '*.txt'):
		with codecs.open(os.path.join(dirpath, filename),'r',encoding="utf-8")as f:
			for tweet in f:
				try :
					tweet_id = tweet.split("\t")[0]
					tweet = tweet.split("\t")[1]
					counter += 1
					# حذف منشن یا ااسمی افراد
					tweet= re.sub(r'@[A-Za-z0-9_]+', '',tweet)
					# حذف یوآرال
					tweet= re.sub(r'https?://[^ ]+', '', tweet)
					# حذف یوآرال
					tweet= re.sub(r'www.[^ ]+', '', tweet)
					# حذف کاراکترهای خاص
					tweet = re.sub(r"[a-zA-Z!$()&@0-9:\\#/|{}<>?؟=.\"\'…»«;,،]", "", tweet)

					emoji_pattern = u'([🤦🤗🤪🤷🤘🤣🤔🤐🤚🤢🤡])|([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])|([\U0001F1E0-\U0001F1FF])|([\U00002702-\U000027B0])|([\U000024C2-\U0001F251])'
					tweet=re.sub(emoji_pattern, '', tweet)


					if len(tweet.strip()) > 0 :
						with codecs.open("output/step1/"+filename, 'a',encoding="utf-8") as fout:
							if "\n" not in tweet :
								fout.write(tweet_id+"\t"+tweet+"\n")
							else :
								fout.write(tweet_id+"\t"+tweet)


					print(str(counter))
				except BaseException as e :
					print("Error on_data: %s" % str(e))
					f.flush()
