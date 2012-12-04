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


#initialiations

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
freqList = {}
wordList = []
wordsintweets =[]


#entry point method for the text processing.
#called by both the train and classify methods to process the tweets.
# input parameter flow contains values 1 or 2.
#1 indicates train flow and 2 indicates test flow.

def process(flow):

    #load the necessary files.
    #training files are split into 4, one for each category.

    if flow==2:
        filenames=['../flatfiles/test.txt']
    else:
        filenames=['../flatfiles/sports_xl','../flatfiles/finance_xl','../flatfiles/entertain_xl','../flatfiles/technology_xl']

    #load the nltk wordl ist into memory.
    wordList = nltk.corpus.words.words()

    #load stop words into memory
    #since the stop word filtering is done after processing of tweets,
    #stop words are also stemmed

    stopwordsfile = open('../flatfiles/stopwords.txt')
    stopwords = set([word for word in stopwordsfile.read().split('\n')])
    stopwords = [porter.stem(s) for s in stopwords]

    #temporary variables for processing.
    lineno = 0
    catId = 0
    wordId = 0
    maxwordid=0
    wordlist=[]

    #Test flow
    if flow==2:
        #file contating all the words.
        #as new word appears, it is appended to this list.
        wf=open("../flatfiles/wordset",'a+')
        wf.write('\n')
        df=open("../flatfiles/testdocset",'w')
        maxwordid=0
        for entry in wf:
            splitEnt=entry.partition('\t')
            if int(splitEnt[0])>int(maxwordid):
                maxwordid=splitEnt[0]
            wordlist.append(str(splitEnt[2]).strip())
    else:
        wf=open("../flatfiles/wordset",'w')
        df=open("../flatfiles/docset",'w')

    maxwordId=int(maxwordid)
    for f in filenames:
        #assign all tweets to category 0 for test
        #else assign the appropriate cat id.
        if flow==2:
            catId=0
        else:
            catId += 1

        #detect language
        #this is done to filter out all non english tweets
        #this is because, our text processing is only for english words.
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

                #use porters stemming logic to stem the words and filter stop words
                list = [porter.stem(word)  for word in unigrams if word]
                list = [word for word in list if word not in stopwords]

                #creat bigrams
                bigrams = [list[i] + " " + list[i + 1] for i in range(len(list) - 1)]
                wordCount = {}

                #the final list of words is the set of unigrams and bigrams
                allTokens = list + bigrams

                #Calculate frequency of each word
                [wordCount.__setitem__(w,1+wordCount.get(w,0)) for w in allTokens]
                for w in wordCount.keys():
                    if w not in wordlist:
                        maxwordId +=1
                        wordlist.append(w)
                        wf.write(str(maxwordId)+"\t"+str(w)+'\n')
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


#module to remove punctuations
def removePunctuations(tokens):
    returnlist = []
    #finds occurances of '--'
    pattern = re.compile(r"(-)\1{1,}", re.DOTALL)
    for token in tokens:
        #weeds out urls
        if token.startswith('http:'):
            continue
        #retains only ', - and #
        # #is used for hastags
        # ' and - are part of names (potentially)
        for punct in string.punctuation:
            if not (punct == '\'' or punct == '-' or punct=='#'):
                token = token.replace(punct, '')
                token = token.rstrip(punct)
            elif len(pattern.findall(token)) > 0:
                continue
        if len(token) > 0:
            returnlist.append(token.rstrip('\n'))
    return returnlist

