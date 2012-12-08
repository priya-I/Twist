'''
Created on Nov 9, 2012
Modified on Nov 29, 2012 --Priya

@author: Priya, Sonali
'''
from liblinearutil import *
from sklearn.metrics import precision_recall_fscore_support
import codecs

def cacheTweetsInList(maxWords, maxTweets,flow):
    if flow==1:
        docf=open("../flatfiles/docset")
    else:
        docf=open("../flatfiles/testdocset")

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
        X=[]
        f = open('../flatfiles/trainAll.txt', 'w')
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
        f.close()


def createTestFile(docwords,docCatIds,maxTweets):
    f = open('../flatfiles/testf.txt', 'w')
    df=open('../flatfiles/testdocset')
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
    labels,features=svm_read_problem('../flatfiles/trainSports.txt')
    options='-s 6 -c 5'
    m=train(labels,features,str(options))
    p_label, p_acc, p_val = predict(labels, features, m)
    save_model('sports.model',m)

    labels,features=svm_read_problem('../flatfiles/trainFin.txt')
    options='-s 6 -c 5'
    m1=train(labels,features,str(options))
    p_label, p_acc, p_val = predict(labels, features, m1)
    save_model('finance.model',m1)

    labels,features=svm_read_problem('../flatfiles/trainEnt.txt')
    options='-s 6 -c 5'
    m2=train(labels,features,str(options))
    p_label, p_acc, p_val = predict(labels, features, m2)
    save_model('entertainment.model',m2)

    labels,features=svm_read_problem('../flatfiles/trainTech.txt')
    options='-s 6 -c 5'
    m3=train(labels,features,str(options))
    p_label, p_acc, p_val = predict(labels, features, m3)
    save_model('technology.model',m3)
    testSVM()

def testSVM(flag=None):
    m=load_model('sports.model')
    labelsS,featuresS=svm_read_problem('../flatfiles/testf.txt')
    s_label, p_acc, p_val = predict(labelsS, featuresS, m)
    print "Sports:  "+str(s_label)

    m1=load_model('finance.model')
    labelsF,featuresF=svm_read_problem('../flatfiles/testf.txt')
    f_label, p_acc, p_val = predict(labelsF, featuresF, m1)
    print "Finance:  "+str(f_label)

    m2=load_model('entertainment.model')
    labelsE,featuresE=svm_read_problem('../flatfiles/testf.txt')
    e_label, p_acc, p_val = predict(labelsE, featuresE, m2)
    print "Entertainment:  "+str(e_label)

    m3=load_model('technology.model')
    labelsT,featuresT=svm_read_problem('../flatfiles/testf.txt')
    t_label, p_acc, p_val = predict(labelsT, featuresT, m3)
    print "Technology:  "+str(t_label)

    outf=open('../outputlabels','w+')
    i=0
    for eachval in s_label:
        outf.write(str(s_label[i])+","+str(f_label[i])+","+str(e_label[i])+","+str(t_label[i]))
        i+=1
        outf.write("\n")
    outf.close()
    oplabels=svmOutput()
    return oplabels

def svmOutput():
    category=['Sports','Finance','Entertainment','Technology']
    testf = codecs.open('../flatfiles/test.txt','r',encoding='UTF-8')
    labelsf=open('../outputlabels','r')
    tweetLabel=[]
    outputLabels=[]
    for labels in labelsf:
        labelsT=[]
        labels=labels.split(',')
        for label in labels:
            if int(float(label))==-1:
                labelsT.append('Other')
            else:
                labelsT.append(category[int(float(label))-1])
        tweetLabel.append(labelsT)
    i=0

    with open("../outputCat",'w') as of:
        for tweet in testf:
            try:
                showLabel=''
                otherCount=0
                count=0
                #print tweetLabel[i]
                for each in tweetLabel[i]:
                   #print each
                   if (each!='Other'):
                         if showLabel=='':
                             showLabel=each
                         else:
                            showLabel=showLabel+'-'+each
                   if (each=='Other'):
                          otherCount+=1
                if otherCount==4:
                    showLabel='Other'
                print showLabel
               # print str(showLabel)+' -> '+tweet+'\n'
                #of.write(showLabel+' -> '+tweet+'\n')
                outputLabels.append((showLabel,tweet))
            except IndexError:
                print 'INVALID TWEET'
                of.write('INVALID ->'+tweet+'\n')
            i+=1
    of.close()
    return outputLabels
