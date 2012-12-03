__author__ = 'priya'

from nlp import TextProcessing as tp
from svmProc import SVMProcessing as svmp


def classify(flag=None):
    #Pre-process tweets
    wordId,tweetId=tp.process(2)
    #TF-IDF
    docwords,docCatIds=svmp.cacheTweetsInList(wordId,tweetId,2)
    #SVM Processing
    #1. Create libSVM file
    svmp.createTestFile(docwords,docCatIds,tweetId)
    #2. Train the SVM
    if flag is not None:
        return svmp.testSVM(1)
    else:
        svmp.testSVM()

def train():
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

if __name__=='__main__':
    flow=input("1.Train 2.Classify")
    if flow==1:
        train()
    elif flow==2:
       classify()
    else:
        print "nothing to do here"
