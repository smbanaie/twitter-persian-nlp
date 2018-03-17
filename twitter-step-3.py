# -*- coding: utf-8 -*-import twitter_config
import os,fnmatch,codecs
import re
import glob, os
import pandas as pd

# path = r'output/step1'
# all_rec = glob.iglob(os.path.join(path, "*.txt"), recursive=True)
# dataframes = (pd.read_csv(f) for f in all_rec)
# df = pd.concat(dataframes, ignore_index=True)
#
# df.head()
def avg_word(sentence):
  words = str(sentence).split()
  return (sum(len(word) for word in words)/len(words))

df2 = pd.read_csv("output/step1/2018-03-17.txt",sep="\t",encoding="utf8",header=None,names=["ID","Text"])
df2['word_count'] = df2['Text'].apply(lambda x: len(str(x).split(" ")))
print (df2[["Text","word_count"]])
df2['avg_word'] = df2['Text'].apply(lambda x: avg_word(x))
print (df2[["Text","word_count","avg_word"]])
freq = pd.Series(' '.join(df2['Text']).split()).value_counts()[:30]
print(freq)

freq = list(freq.index)
df2['Text2'] = df2['Text'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
df2.append(df2["Text2"])
print(df2.head())
# print(df2['Text'])
#
# from persian_wordcloud.wordcloud import PersianWordCloud
# tweet_string = []
# for t in df2.Text:
#     tweet_string.append(t)
# tweet_string = pd.Series(tweet_string).str.cat(sep=' ')
# print(tweet_string[:2000])
# wordcloud = PersianWordCloud(
#     only_persian=True,
#     max_words=100,
#     stopwords=None,
#     margin=0,
#     width=800,
#     height=800,
#     min_font_size=1,
#     max_font_size=500,
#     background_color="black"
# ).generate(tweet_string)
#
# pd.DataFrame.to_csv(r'F:\My GitHub Repos\twitter-persian-nlp\output\step2\tweets_2.txt',sep='\t', encoding='utf-8')
# from persian_wordcloud.wordcloud import arabic_reshaper
# from bidi.algorithm import get_display
# from arabic_reshaper import arabic_reshaper
#
# image = wordcloud.to_image()
# image.show()
# image.save('en-fa-result.png')