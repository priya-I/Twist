#!/usr/bin/python
from database import Database, TestDatabase


__author__ = 'rahmaniacc'


##################################################
# 1. Generate Unigrams                           #
# 2. Filter punctuations.                        #
# 3. Reduce strings. spell correct, stem, reduce #
# 4. Generate bigrams                            #
# 5. Stop words removal                          #
#   Pending items                                #
#   1. singleton implementation for word list    #
#   2.Top suggestoin for spelling                #
##################################################


import nltk
import string
import stemming.porter2 as porter

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
freqList = {}
wordList = []
wordsintweets =[]

def process(flow):
    if flow==2:
        #TestDatabase.clear()
        filenames=['./flatfiles/test.txt']
    else:
        filenames=['./flatfiles/inputtweets','./flatfiles/inputfin']
    wordList = nltk.corpus.words.words()
    stopwordsfile = open('./flatfiles/stopwords.txt')
    stopwords = set([word for word in stopwordsfile.read().split('\n')])
    stopwords = [porter.stem(s) for s in stopwords]
    lineno = 0
    catId = 0
    wordId = 1
    #filenames = ['sport.txt','finance.txt']
    #filenames=['../flatfiles/inputtweets','../flatfiles/inputfin']

    for f in filenames:
        if flow==2:
            catId=0
        else:
            catId += 1
        with open(f) as tweet_list:


            for line in tweet_list:
                wordidList = []
                freqList = []
                lineno += 1
                print lineno
                #input = 'hello, how are you ? I\'m jumping with joy because she is soooooooooo cuuuttee and !!!!.'
                #unigrams = [spellcheck.spellcheck(word) for word in removePunctuations(line.split())]
                unigrams = [word for word in removePunctuations(line.split())]
                unigrams = [u for u in unigrams if unigrams and len(unigrams)>0]
                list = [porter.stem(word)  for word in unigrams if word]
                list = [word for word in list if word not in stopwords]
                bigrams = [list[i] + " " + list[i + 1] for i in range(len(list) - 1)]

                wordCount = {}
               # allTokens = list + bigrams
                allTokens=list
                #print [i for i in allTokens]
                [wordCount.__setitem__(w,1+wordCount.get(w,0)) for w in allTokens]

                for w in wordCount.keys():
                    if w not in wordsintweets:
                        wordsintweets.append(w)
                        wordidList.append((wordId,w))
                        freqList.append((lineno,catId,wordId,wordCount[w]))
                        wordId +=1

                if flow==1:
                    Database.InsertWords(wordidList)
                    Database.InsertTweets(freqList)
                elif flow==2:
                    TestDatabase.InsertWords(wordidList)
                    TestDatabase.InsertTweets(freqList)





def findSuggestions(word):

    return  0
#    d = {}
#    freqList = getwordList()
#    for w,f in freqList.items():
#        if w in suggestions_filtered:
#            d[w] = f
#    return d[sorted(d, key=d.get, reverse=True)[0]]

def getwordList():
    words = open('word.txt')
    return  [(line.split('\t')[1], line.split('\t')[0]) for line in words]


def removePunctuations(tokens):
    returnlist = []
    for token in tokens:
        for punct in string.punctuation:
            if not (punct == '\'' or punct == '-'):
                token = token.replace(punct, '')
                token = token.rstrip(punct)
        if len(token) > 0:
            returnlist.append(token.rstrip('\n'))
    return returnlist

