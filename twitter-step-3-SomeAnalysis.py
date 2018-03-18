# -*- coding: utf-8 -*-import twitter_config
import os,fnmatch,codecs
import re
import glob, os
import pandas as pd

path = r'output/step1'
all_rec = glob.iglob(os.path.join(path, "*.txt"), recursive=True)
dataframes = (pd.read_csv(f,sep="\t",encoding="utf8",header=None,names=["ID","Text"]) for f in all_rec)
df = pd.concat(dataframes, ignore_index=True)




def avg_word(sentence):
  words = str(sentence).split()
  return (sum(len(word) for word in words)/len(words))

print("#"*50)
df['avg_word'] = df['Text'].apply(lambda x: avg_word(x))
print(df.head())

print("#"*50)
df['word_count'] = df['Text'].apply(lambda x: len(str(x).split(" ")))
print(df.head())

print("$"*50)
short_tweets = df[df["word_count"] < 5]
print(short_tweets.head())
short_tweets.to_csv(r'output\step2\short_texts.txt',sep='\t',index=False, encoding='utf-8',header=True,columns=["ID","Text"])
short_tweets2 = df[(df["word_count"] < 10) & (df["avg_word"]>5)]
print(short_tweets2.head())


print("&"*50)
freq = pd.Series(' '.join(df['Text']).split()).value_counts()[:30]
print(freq)

print("&"*50)
freq = list(freq.index)
df['Text'] = df['Text'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))

print("#"*50)
freq2 = pd.Series(' '.join(df['Text']).split()).value_counts()[-50:]
print(freq2)


df.to_csv(r'output\step2\tweets_all.txt',sep='\t',index=False, encoding='utf-8',header=True,columns=["ID","avg_word","word_count","Text"])
