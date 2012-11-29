__author__ = 'priya'

'''
Created on Sep 30, 2012
@note: This file downloads the list of followers of a user into a file named after the user.
@author: priya
'''
import tweepy
import Keys

def getFollowers(username1):
    auth=tweepy.OAuthHandler(Keys.consumer_key,Keys.consumer_secret)
    auth.set_access_token(Keys.access_token, Keys.access_token_secret)
    api=tweepy.API(auth)

    #Get the user object of the username specified. If no such user exists, throw error and return
    try:
        user1=api.get_user(screen_name=username1)
    except:
        print "Invalid user name!"
        return
    print user1.name

    #Create a file with the name same as that of the user specified
    f1=open(username1,"w+")
    cursor1=tweepy.Cursor(user1.followers)
    iterator1=cursor1.iterator
    next_cursor=iterator1.next_cursor

    '''Try getting the followers using the cursor.
    If there is an exception, set the next_cursor to the same point where the exception occurred
    and continue.
    '''
    while(next_cursor!=0):
        try:
            followers1=iterator1.next()
            for follower1 in followers1:
                f1.write(follower1.screen_name+"\n")
            next_cursor = iterator1.next_cursor
        except:
            cursor1=tweepy.Cursor(user1.followers)
            iterator1=cursor1.iterator
            iterator1.next_cursor=next_cursor

    f1.close()