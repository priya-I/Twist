'''
Created on Nov 9, 2012
Modified on Nov 29, 2012 --Priya

@author: Priya, Sonali
'''
from svmutil import *
from liblinearutil import *

def createGlobalDictionary(maxWords, maxTweets,flow):
    gdf=open("globalDict",'w')
    if flow==1:
        docf=open("docset")
        categories=['','sports','finance']
    else:
        docf=open("testdocset")
        categories=['uncategorized']

    tweetWords={}
    docCats={}
    docCatIds={}

    #This portion gets the entries from the Tweets File.
    for entry in docf:
        theTweetEntry=entry.split()
        tweetID=theTweetEntry[0]
        catID=theTweetEntry[1]
        wordIndexInTweet=theTweetEntry[2]
        if tweetWords.get(long(tweetID)) is None:
            tweetWords[long(tweetID)]=wordIndexInTweet
        else:
            tweetWords[long(tweetID)]= str(tweetWords[long(tweetID)])+"\t"+str(wordIndexInTweet)
        docCats[long(tweetID)]=categories[long(catID)]
        docCatIds[long(tweetID)]=long(catID)

    #This portion makes entries into the global dictionary
    print "Max Words "+str(maxWords)
    for tweet in range(1,maxTweets+1):
        print "Tweet id: "+str(tweet)
        docentry=tweetWords[tweet]
        wordsInThisTweet=docentry.split()
        for word in range(1,maxWords+1):
            if str(word) in wordsInThisTweet:
                flag=1
            else:
                flag=0
            gdf.write(str(flag)+" ")
            #For input into scikit-LR
            #if i==maxWords:
            #   gdf.write(str(flag)+","+docCats[j])
        gdf.write("\n")
    return tweetWords,docCatIds


def createTrainFile(docwords,docCatIds):
        f = open('./flatfiles/trainf.txt', 'w')
        gf=open('./globalDict')
        gf.seek(0)
        tweetid=1
        for features in gf:
            catid=docCatIds[tweetid]
            words=docwords[tweetid]
            features=features.split(",")
            f.write(str(catid))
            for word in words.split():
                f.write(" "+str(word)+":"+str(features[int(word)-1])+" ")
            f.write("\n")
            tweetid+=1
        gf.close()
        f.close()


def createTestFile(docwords,docCatIds):
    f = open('./flatfiles/testf.txt', 'w')
    gf=open('./globalDict')
    gf.seek(0)
    tweetid=1
    for features in gf:
        catid=0
        words=docwords[tweetid]
        features=features.split(' ')
        f.write(str(catid))
        for word in words.split():
            f.write(" "+str(word)+":"+str(features[int(word)-1])+" ")
        f.write("\n")
        tweetid+=1
    gf.close()
    f.close()

def trainliblinear():
    labels,features=svm_read_problem('./flatfiles/trainf.txt')
    m=train(labels,features,'-c 4 -e 0.1')
    #comment out the line below if using cross validation(-v)
    p_label, p_acc, p_val = predict(labels, features, m)
    save_model('TwoCatModel.model',m)

def trainSVM():
    labels,features=svm_read_problem('./flatfiles/trainf.txt')
    m=svm_train(labels,features,'-c 4 -t 0 -e 0.1 -m 800 -v 10')
    #p_label, p_acc, p_val = svm_predict(labels, features, m) --comment out if using cross validation
    #svm_save_model('TwoCatsModel.model',m)

def testSVM():
    m=load_model('TwoCatsModel.model')
    #labels,features=svm_read_problem('/home/priya/Twist/flatfiles/testf.txt')
    labels,features=svm_read_problem('./flatfiles/testf.txt')
    p_label, p_acc, p_val = predict(labels, features, m)
    ACC, MSE, SCC = evaluations(labels, p_label)
    print p_label
    print "Results"+ str(ACC)+" "+str(MSE)+" "+str(SCC)
    svmOutput(p_label)


def svmOutput(p_label):
    category=['Sports','Finance']
    with open("outputCat") as of:
        for eachLabel in p_label:
            print category[eachLabel]+"\n"
            of.write(category[eachLabel]+"\n")
