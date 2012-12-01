#!/usr/bin/python

__author__ = 'rahmaniacc','priya'


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
import spellcheck
import langid
import re

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
freqList = {}
wordList = []
wordsintweets =[]

def process(flow):
    if flow==2:
        filenames=['./flatfiles/test.txt']
    else:
        filenames=['./flatfiles/sports_smaller','./flatfiles/finance_smaller']
    wordList = nltk.corpus.words.words()
    stopwordsfile = open('./flatfiles/stopwords.txt')
    stopwords = set([word for word in stopwordsfile.read().split('\n')])
    stopwords = [porter.stem(s) for s in stopwords]
    lineno = 0
    catId = 0
    wordId = 0
    maxwordid=0
    wordlist=[]
    if flow==2:
        wf=open("wordset",'r+a')
        df=open("testdocset",'w')
        maxwordid=0
        for entry in wf:
            splitEnt=entry.partition('\t')
            if int(splitEnt[0])>int(maxwordid):
                maxwordid=splitEnt[0]
            wordlist.append(str(splitEnt[2]).strip())
    else:
        wf=open("wordset",'w')
        df=open("docset",'w')
    maxwordId=int(maxwordid)
    for f in filenames:
        if flow==2:
            catId=0
        else:
            catId += 1
        langDObj=langid.LangDetect()
        with open(f) as tweet_list:
            for line in tweet_list:
                lineno += 1
                print lineno

                #lang id
                '''if langDObj.detect(line) is not 'en':
                    #print 'not english'
                    continue
                '''
                #remove punctuations,urls and convert to lowe case
                unigrams = [word.lower() for word in removePunctuations(line.split())]

                #unigrams = [spellcheck.spellcheck(u) for u in unigrams if unigrams and len(unigrams)>0]
                unigrams = [u for u in unigrams if unigrams and len(unigrams)>0]
                list = [porter.stem(word)  for word in unigrams if word]
                list = [word for word in list if word not in stopwords]
                bigrams = [list[i] + " " + list[i + 1] for i in range(len(list) - 1)]
                wordCount = {}
                allTokens = list + bigrams
                [wordCount.__setitem__(w,1+wordCount.get(w,0)) for w in allTokens]
                for w in wordCount.keys():
                    if w not in wordlist:
                        maxwordId +=1
                        wordlist.append(w)
                        wf.write('\n'+str(maxwordId)+"\t"+str(w))
                        wordId=maxwordId
                    else:
                        wordId=wordlist.index(w)+1
                    df.write(str(lineno)+"\t"+str(catId)+"\t"+str(wordId)+"\t"+str(wordCount[w])+"\n")
    wf.close()
    df.close()
    return maxwordId,lineno

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
    pattern = re.compile(r"(-)\1{1,}", re.DOTALL)
    for token in tokens:
        if token.startswith('http:'):
            continue
        for punct in string.punctuation:
            if not (punct == '\'' or punct == '-' or punct=='#'):
                token = token.replace(punct, '')
                token = token.rstrip(punct)
            elif len(pattern.findall(token)) > 0:
                continue
        if len(token) > 0:
            returnlist.append(token.rstrip('\n'))
    return returnlist

