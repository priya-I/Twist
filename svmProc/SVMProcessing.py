'''
Created on Nov 9, 2012
Modified on Nov 29, 2012 --Priya

@author: Priya, Sonali
'''
from svmutil import *
from liblinearutil import *
from sklearn.metrics import precision_recall_fscore_support


def cacheTweetsInList(maxWords, maxTweets,flow):
    if flow==1:
        docf=open("docset")
    else:
        docf=open("testdocset")

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
        docCatIds[long(tweetID)]=long(catID)

    return tweetWords,docCatIds


def createTrainFile(docwords,docCatIds,maxTweets):
        f = open('../flatfiles/trainAll.txt', 'w')
        df=open('../docset')
        for tweetid in range(1,int(maxTweets)+1):
            try:
                catid=docCatIds[tweetid]
                words=docwords[tweetid]
                f.write(str(catid))
                for word in words.split():
                    f.write(" "+str(word)+":"+str(1)+" ")
                f.write("\n")
            except KeyError:
                print tweetid
                f.write(str(catid))
                for word in words.split():
                    f.write(" "+str(word)+":"+str(1)+" ")
                f.write("\n")
        df.close()
        f.close()


def createTestFile(docwords,docCatIds,maxTweets):
    f = open('../flatfiles/testf.txt', 'w')
    df=open('../testdocset')
    for tweetid in range(1,int(maxTweets)+1):
        try :
            catid=docCatIds[tweetid]
            words=docwords[tweetid]
        except KeyError:
            f.write(str(0)+" "+str(0)+":"+str(1)+" ")
            f.write("\n")
            continue
        f.write(str(catid))
        for word in words.split():
            f.write(" "+str(word)+":"+str(1)+" ")
        f.write("\n")
    df.close()
    f.close()

def trainliblinear():
    #labels,features=svm_read_problem('../flatfiles/trainf.txt')
    labels,features=svm_read_problem('../flatfiles/trainAll.txt')

    #m=train(labels,features,'-c 4 -e 0.1 -v 5')
    #m=train(labels,features,'-c 10 -w1 1 -w2 5')
    costs={10,5}
    types={5,6,7}
    of = open('../flatfiles/trainOutput.txt', 'w')

    ################################################
    exp_label=[4,4,1,1,2,1,1,1,2,1,1,3,2,2,2,4,4,2,2]
    for cost in costs:
        for type in types:
            #options='-s '+str(type)+' -c '+str(cost)+' -v '+str(10)+' -q'
            options='-s '+str(type)+' -c '+str(cost)+' -q'
            #options='-s 7 -c 0.01 -q'
            print options
            m=train(labels,features,str(options))
            p_label, p_acc, p_val = predict(labels, features, m)
            #save_model('SFETModel.model',m)
            #ACC,MSE,SCC=evaluations(labels,p_label)
            #testSVM()
            #print classification_report(labels, p_label)
            ##############################
            labels1,features1=svm_read_problem('../flatfiles/testf.txt')
            p_label1, p_acc, p_val = predict(labels1, features1, m)
            prec,rec,f1,sup = precision_recall_fscore_support(exp_label, p_label1, beta=1.0, labels=None, pos_label=None, average='macro')
            rec= "%0.2f" % rec
            prec ="%0.2f" % prec
            print "Recall "+str(rec)+"\t"+"Precision"+str(prec)
            of.write("\t"+str(rec)+"\t"+str(prec))
            of.write("\n")
            svmOutput(p_label1)
    of.close()
            ##############################################

def trainLibLinear():
    #labels,features=svm_read_problem('../flatfiles/trainf.txt')
    labels,features=svm_read_problem('../flatfiles/trainAll.txt')
    options='-s 6 -c 5'
    m=train(labels,features,str(options))
    p_label, p_acc, p_val = predict(labels, features, m)
    #prec,rec,f1,sup = precision_recall_fscore_support(labels, p_label, beta=1.0, labels=None, pos_label=None, average='macro')
    save_model('SFETClassModel.model',m)

def plotgraph():
    searchfile = open("../flatfiles/trainfoutput4classes.txt", "r")
    for line in searchfile:
        if "avg / total" in line: print line
    searchfile.close()

def testSVM(flag=None):
    #m=load_model('SFETClassModel.model')
    m=load_model('../SFETModel.model')
    labels,features=svm_read_problem('../flatfiles/testf.txt')
    p_label, p_acc, p_val = predict(labels, features, m)
    svmOutput(p_label)
    if flag is not None:
        return p_label


def svmOutput(p_label):
    category=['Sports','Finance','Entertainment','Technology']
    testf=open('../flatfiles/test.txt')
    i=0
    with open("../outputCat",'w') as of:
        for tweet in testf:
            try:
                print category[int(p_label[i])-1]
                of.write(category[int(p_label[i])-1]+'->'+tweet+'\n')
            except IndexError:
                print 'INVALID TWEET'
                of.write('INVALID ->'+tweet+'\n')
            i+=1
    of.close()
