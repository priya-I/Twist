__author__ = 'priya'

'''
Flows A. Train B. Test C. Modify
A. Train
1. Initialize database. Call database.py
2. Stream Twitter data
3. Call TextProcessing.py
4. libsvminput
5. testSVM

B. Test
1. Initialize testdatabase. Call database.py
2. Stream Twitter data
3. Call TextProcessing.py
4. libsvminput
5. testSVM

C. Modify
'''
from nlp import TextProcessing as tp
from svmProc import SVMProcessing as svmp

if __name__=='__main__':
    flow=input("1.Train 2.Classify 3.Re-classify")
    if flow==1:
        #Pre-process tweets
        wordId,tweetId=tp.process(1)
        #TF-IDF
        docwords,docCatIds=svmp.createGlobalDictionary(wordId,tweetId,flow)
        #SVM Processing
        #1. Create libSVM file
        svmp.createTrainFile(docwords,docCatIds)
        #2. Train the SVM
        #svmp.trainSVM()
        svmp.trainliblinear()
    elif flow==2:
        #Pre-process tweets
        wordId,tweetId=tp.process(2)
        #TF-IDF
        docwords,docCatIds=svmp.createGlobalDictionary(wordId,tweetId,flow)
        #SVM Processing
        #1. Create libSVM file
        svmp.createTestFile(docwords,docCatIds)
        #2. Train the SVM
        svmp.testSVM()
    else:
        print "nothing to do here"
