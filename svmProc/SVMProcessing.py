'''
Created on Nov 9, 2012

@author: Priya, Sonali
'''
import sqlite3 as lite
from svmutil import *
from svmProc import *

def createTrainFile():
        con = lite.connect('./database/twist.db')
        f = open('./flatfiles/trainf.txt', 'w')
        with con:
        
            cur = con.cursor()    
            cur.execute("SELECT DISTINCT TWEETID FROM Documents")
            docrows = cur.fetchall()
            #print docrows.length()
            
            for i in docrows:
                cur.execute("SELECT DISTINCT(CATID) FROM Documents WHERE TWEETID=?",(i[0],))
                catid = cur.fetchone()
                f.write(str(catid[0])+" ")
                print "catid"+str(catid[0])+" "
                
                cur.execute("SELECT WORDID FROM Documents WHERE TWEETID=?",(i[0],))
                wordrows = cur.fetchall()
                for j in wordrows:
                    print j[0]
                    cur.execute("SELECT TFIDF FROM GlobalDict WHERE TWEETID=? AND WORDID=?",(i[0],j[0]))
                    tfidf = cur.fetchone()
                    f.write(str(j[0])+":"+str(tfidf[0])+" ");
                    print str(j[0])+":"+str(tfidf[0])+" "
                    
                f.write("\n")
                
            f.close()


def createTestFile():
    con = lite.connect('/home/priya/Twist/database/twist.db')
    f = open('./flatfiles/testf.txt', 'w')
    with con:

        cur = con.cursor()
        cur.execute("SELECT DISTINCT TWEETID FROM TestDocuments")
        docrows = cur.fetchall()
        #print docrows.length()

        for i in docrows:
            cur.execute("SELECT DISTINCT(CATID) FROM TestDocuments WHERE TWEETID=?",(i[0],))
            catid = cur.fetchone()
            f.write(str(catid[0])+" ")
            print "catid"+str(catid[0])+" "

            cur.execute("SELECT WORDID FROM TestDocuments WHERE TWEETID=?",(i[0],))
            wordrows = cur.fetchall()
            for j in wordrows:
                print j[0]
                cur.execute("SELECT TFIDF FROM TestGlobalDict WHERE TWEETID=? AND WORDID=?",(i[0],j[0]))
                tfidf = cur.fetchone()
                f.write(str(j[0])+":"+str(tfidf[0])+" ");
                print str(j[0])+":"+str(tfidf[0])+" "

            f.write("\n")

        f.close()
        

def trainSVM():

    labels,features=svm_read_problem('./flatfiles/trainf.txt')

    m=svm_train(labels,features,'-s 0 -t 0 -c 1')
    p_label, p_acc, p_val = svm_predict(labels, features, m)
    svm_save_model('TwoCatsModel.model',m)
    print p_label

def testSVM():
    m=svm_load_model('TwoCatsModel.model')
    labels,features=svm_read_problem('/home/priya/Twist/flatfiles/testf.txt')
    p_label, p_acc, p_val = svm_predict(labels, features, m)

    ACC, MSE, SCC = evaluations(labels, p_label)
    print p_label
    print ACC, MSE, SCC