'''
Created on Nov 9, 2012
Modified on Nov 29, 2012 --Priya

@author: Priya, Sonali
'''
from svmutil import *
from liblinearutil import *

def createGlobalDictionary(maxWords, maxTweets,flow):
    #gdf=open("./globalDict",'a+')

    if flow==1:
        docf=open("docset")
        #categories=['','sports','finance']
    else:
        docf=open("testdocset")
        #categories=['uncategorized']

    tweetWords={}
    #docCats={}
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
        #docCats[long(tweetID)]=categories[long(catID)]
        docCatIds[long(tweetID)]=long(catID)

    #This portion makes entries into the global dictionary
    '''
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
        '''
    return tweetWords,docCatIds


def createTrainFile(docwords,docCatIds,maxTweets):
        f = open('./flatfiles/trainf.txt', 'w')
        df=open('./docset')
        for tweetid in range(1,int(maxTweets)+1):
            catid=docCatIds[tweetid]
            words=docwords[tweetid]
            f.write(str(catid))
            for word in words.split():
                f.write(" "+str(word)+":"+str(1)+" ")
            f.write("\n")
        df.close()
        f.close()


def createTestFile(docwords,docCatIds,maxTweets):
    f = open('./flatfiles/testf.txt', 'w')
    df=open('./testdocset')
    for tweetid in range(1,int(maxTweets)+1):
        catid=docCatIds[tweetid]
        words=docwords[tweetid]
        f.write(str(catid))
        for word in words.split():
            f.write(" "+str(word)+":"+str(1)+" ")
        f.write("\n")
    df.close()
    f.close()

def trainliblinear():
    labels,features=svm_read_problem('./flatfiles/trainf.txt')
    #m=train(labels,features,'-c 4 -e 0.1 -v 5')
    m=train(labels,features,'-c 10 -w1 1 -w2 5')
    #m=train(labels,features,'-s 0 -v 5')
    #m=train(labels,features,'-v 5 -e 0.001')
    #comment out the line below if using cross validation(-v)
    p_label, p_acc, p_val = predict(labels, features, m)
    save_model('SFModel.model',m)

def trainSVM():
    labels,features=svm_read_problem('./flatfiles/trainf.txt')
    m=svm_train(labels,features,'-c 4 -t 0 -e 0.1 -m 800 -v 10')
    #p_label, p_acc, p_val = svm_predict(labels, features, m) --comment out if using cross validation
    #svm_save_model('TwoCatsModel.model',m)

def testSVM():
    m=load_model('SFModel.model')
    #labels,features=svm_read_problem('/home/priya/Twist/flatfiles/testf.txt')
    labels,features=svm_read_problem('./flatfiles/testf.txt')
    p_label, p_acc, p_val = predict(labels, features, m)
    ACC, MSE, SCC = evaluations(labels, p_label)
    print p_label
    print "Results"+ str(ACC)+" "+str(MSE)+" "+str(SCC)
    svmOutput(p_label)


def svmOutput(p_label):
    category=['Sports','Finance']
    testf=open('./flatfiles/test.txt')
    i=0
    with open("outputCat",'w') as of:
        for tweet in testf:
            print category[int(p_label[i])-1]
            of.write(category[int(p_label[i])-1]+'->'+tweet+'\n')
            i+=1
    of.close()
