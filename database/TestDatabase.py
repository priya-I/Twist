'''
Created on Nov 7, 2012

@author: sonali
'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import math
import datetime

maxFreqInDoc={}
noOfDocsWithWord={}


def InitializeTestDB():
    try:
        con = lite.connect('/home/priya/Twist/database/twist.db')

        with con:

            cur = con.cursor()
            cur.execute("CREATE TABLE TestDocuments(TWEETID INT,CATID INT,WORDID INT,FREQ INT);")
            cur.execute("CREATE TABLE TestWords(ID INT, WORD TEXT NOT NULL,PRIMARY KEY(WORD));")
            cur.execute("CREATE TABLE TestGlobalDict(TWEETID INT,WORDID INT,TFIDF FLOAT );")
            con.commit()

    except lite.Error, e:

        if con:
            con.rollback()

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if con:
            con.close()



def InsertWords(wordlist):
    try:
        con = lite.connect('/home/priya/Twist/database/twist.db')
    
        with con:
        
            cur = con.cursor()    

            
            try:
                for worden in wordlist:
                   cur.execute("INSERT INTO TestWords VALUES(?, ?);", worden)
            except:
                pass

            con.commit()
        
    except lite.Error, e:
            
            if con:
                con.rollback()
                
            print "Error %s:" % e.args[0]
            sys.exit(1)
            
    finally:
            
            if con:
                con.close()

def InsertTweets(docentries):
     try:
        con = lite.connect('/home/priya/Twist/database/twist.db')
    
        with con:
            cur = con.cursor() 
            for docen in docentries:
               cur.execute("INSERT INTO TestDocuments VALUES(?,?,?,?);", docen)

            con.commit()
        
     except lite.Error, e:
            
            if con:
                con.rollback()
                
            print "Error %s:" % e.args[0]
            sys.exit(1)
            
     finally:
            
            if con:
                con.close()     
     
                

    
def tfidf():
    con = lite.connect('/home/priya/Twist/database/twist.db')
    with con:
        finaltfidf = []
        wcur = con.cursor()
        wcur.execute("SELECT distinct(WORDID) FROM TestDocuments")
        wordrows = wcur.fetchall()
        
        
        wcur.execute("SELECT distinct(TWEETID) FROM TestDocuments")
        docrows = wcur.fetchall()


        for j in docrows:
            wcur.execute("SELECT MAX(FREQ) FROM TestDocuments WHERE TWEETID=? ",(j[0],))
            maxtdf=wcur.fetchone()
            maxFreqInDoc[int(j[0])]=maxtdf[0]

        for i in wordrows:
            wcur.execute("SELECT COUNT(DISTINCT(TWEETID)) FROM TestDocuments WHERE WORDID=?",(i[0],))
            idfd=wcur.fetchone()
            noOfDocsWithWord[int(i[0])]=idfd[0]


        wcur.execute("SELECT COUNT(DISTINCT(TWEETID)) FROM TestDocuments")
        idfn = wcur.fetchone()[0]

    for i in wordrows:
            for j in docrows:
                t = tfidfcalculator(i[0],j[0],idfn)
                finaltfidf.append(t)

    wcur.executemany("INSERT INTO TestGlobalDict values(?,?,?)",finaltfidf);
    con.commit()
           # wcur.execute("INSERT INTO GlobalDict values(?,?,?)",(eachrowt[0],eachroww[0],tfidf))
           # con.commit()
            
def tfidfcalculator(wordID,docID,idfn):

    con = lite.connect('/home/priya/Twist/database/twist.db')
    wordid=int(wordID)
    docid=int(docID)
    with con:
        wcur = con.cursor()
        #print datetime.datetime.now()
        wcur.execute("SELECT FREQ FROM TestDocuments WHERE WORDID=? AND TWEETID=? ",(wordid,docid))
        #print datetime.datetime.now()

        tfd=wcur.fetchone()
        maxtdf=maxFreqInDoc[docid]
        idfd=noOfDocsWithWord[wordid]

       # print "f(d,w) "+str(fdw)
        print wordid , docid
        if  tfd==None:
           return docid,wordid,0
           #wcur.execute("INSERT INTO GlobalDict values(?,?,?)",(docid,wordid,0.0))
           #print wordid, docid
           #con.commit()
        else:
            if maxtdf!=0 and idfd!=0:
                print "******************************WORDID "+str(wordid)+"***************DOCID "+str(docid)
                print "TFD Value: "+str(tfd[0])
                print "MAX TDF Value: "+str(maxtdf)
                print "D value: "+str(idfn)
                print "FDT value: "+str(idfd)
                tfidf = (float(tfd[0])/float(maxtdf))*math.log10(float(idfn)/float(idfd))
                return docid,wordid,tfidf

                #wcur.execute("INSERT INTO GlobalDict values(?,?,?)",(docid,wordid,tfidf))
                #print wordid , docid , tfidf
                #con.commit()

def clear():
    con = lite.connect('/home/priya/Twist/database/twist.db')
    wcur=con.cursor()
    wcur.execute("TRUNCATE TABLE TestWords")
    wcur.execute("TRUNCATE TABLE TestDocuments")
    wcur.execute("TRUNCATE TABLE TestGlobalDict")
