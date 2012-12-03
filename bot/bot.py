__author__ = 'rahmaniac'
#!/usr/bin/env python

import tweepy
import os
import datetime
import app


#set the consumer and athentication tokens
#make it configurable so that it can be input in a seperate properties file.

consumer_key="naoQ7x0eZzmzBQGLvbe6Gg"
consumer_secret="G37X7Q6DBsfa87g63jIWXqe48bC62wrAmiRCooQGig"
access_token="981674924-xO47aVZPA6pLkU7iHvuRgkoZpd3pPJWAsrhHli2f"
access_token_secret="1jJ2J9lAQ98gvihm2m2MpYlhV44SZYqr09z3B8Ug"

#create the tweepy api module  with the authentication keys.

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#auth = tweepy.BasicAuthHandler(username='TwistSports1',password='pythonize')
api = tweepy.API(auth_handler=auth)

#dictionary that saves the tweet id and the tweet
tweetdict = {}


#method  that saves the last tweeted id from the user time line
#this is done so that the bot does not keep classifying previosuly classified tweets
def saveState(statef,currentid):
    since_id = retrievestate(statef)
    if since_id < currentid:
        f = open(statef,'w')
        f.write(str(currentid))
        f.close()

#Retreives the last retweeted id from the file.
#Only tweets with id value greater than this will be sent to the classifier
def retrievestate(statef):
    f = open(statef,'r')
    id = int(f.read())
    f.close()
    return id


#logic for retweet.
#this module takes the classified lables as the nput
#and retweets the tweet along with the category id.

def retweet(labels):

    category=['Sports','Finance','Entertainment','Technology']
    #testf=open('./flatfiles/test.txt')
    testf=open('tempFile.txt')
    tweets = [tweet for tweet in testf.readlines()]
    i=0
    for i in range(0,len(labels)):

        #print ('Retweeting #%d' % (tweets[i],))
        usern,tweet = tweets[i].split('\t')
        print "REtweeting " +tweet
        tw = category[int(labels[i])-1] + ' -> RT @' + usern + ":" + tweet.text
        #tw = 'Sports Tweet -> ' + tweets[i]
        api.update_status(tw[:140])

def main():

    #creation of files
    #1. state.txt  - to save the state of the last tweeted id
    #2. test.txt - contains only tweets. This is fed as input to the classifier.
    #3. tempFile - contains username and tweet in the same order . This is used to retweet the tweet along with the user name.

    since_id = retrievestate('state.txt')
    testfile = open('./flatfiles/test.txt','w+')
    tempFile = open('tempFile.txt','w+')

    #fetch all the user time line.
    tweets = api.home_timeline()
    id= ''

    #iterate through the tweets and write them to the file if the id is > than the last tweeted id.
    for tweet in tweets:
        id = tweet.id
        if tweet.id > since_id and tweet.user.screen_name is not 'TwistSports2':
            tweetdict[tweet.id] = tweet.text
            try:
                testfile.write(tweet.text +  "\n")
                tempFile.write(tweet.user.screen_name + "\t" + tweet.text + "\n")
            except:
                pass

    testfile.close()

    #Save the last tweeted id to the file
    saveState('state.txt',id)

    #call the classify function
    #parameter 1 specifies that it expects a return value.
    labels = app.classify(1)

    #once the classification is done, retweet the classified tweets with their categories.
    retweet(labels)


if __name__ == '__main__':
    main()
