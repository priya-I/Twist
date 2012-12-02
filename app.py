__author__ = 'priya'

from nlp import TextProcessing as tp
from svmProc import SVMProcessing as svmp

if __name__=='__main__':
    flow=input("1.Train 2.Classify")
    if flow==1:
        #Pre-process tweets
        #wordId,tweetId=tp.process(1)
        #TF-IDF
        #docwords,docCatIds=svmp.cacheTweetsInList(wordId,tweetId,flow)
        #SVM Processing
        #1. Create libSVM file
        #svmp.createTrainFile(docwords,docCatIds,tweetId)
        #2. Train the SVM
        #svmp.trainSVM()
        svmp.trainliblinear()
        #svmp.trainLibLinear()
    elif flow==2:
        #Pre-process tweets
        #wordId,tweetId=tp.process(2)
        #TF-IDF
        #docwords,docCatIds=svmp.cacheTweetsInList(wordId,tweetId,flow)
        #SVM Processing
        #1. Create libSVM file
        #svmp.createTestFile(docwords,docCatIds,tweetId)
        #2. Train the SVM
        svmp.testSVM()
    else:
        print "nothing to do here"
