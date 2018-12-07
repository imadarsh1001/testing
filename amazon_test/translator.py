import pandas as pd
from py_translator import Translator

#df = pd.read_csv("m.xml", usecols=['title'])
# df = pd.read_csv("movies.csv", usecols=['title'])
#data=df['title']
# df = pd.read_csv("movies.csv")
# df_s = pd.read_csv("movies.csv", usecols=['synopsis'])
# 
# print(df[0:1])
# print(df['title'])
# print(df)
#print(data)
title=Translator().translate(text='Ich - Einfach unverbesserlich', dest='en').text
titl=Translator().translate(text='Harry Potter und der Orden des PhÃ¶nix', dest='en').text

print(title,'\t',titl)
# for row in range(0,10):
#     liste=data[row]
#     title=Translator().translate(text=liste, dest='en').text
#     # print(liste,title)
#     type(liste)
# title=Translator().translate(text=df['title'][1], dest='en').text

# title.to_csv('movie_a.csv',index=False)
# df.to_csv("movie_list.csv",index=False)
# print(df['title'][1])
# title=Translator().translate(text=df['title'][0:1], dest='en').text
# print(title)

# s=pd.DataFrame(df)
# print(s)
# print(head[df])

# for row in df:
#     print(row)