from flask import Flask
from flask import request
import flask
import tweepy
from nlp import TextProcessing as tp
from svmProc import SVMProcessing as svmp
import codecs
from tweepy import Cursor

app = Flask(__name__)
app.debug = True
#config

CONSUMER_TOKEN = 'IsihqDl0vf9ur6GrWEx67A'
CONSUMER_SECRET = 'h1QHbvnCPbQA8TbzX1wNGmCw7gOofK8QUyJHXUtlo'
CALLBACK_URL = 'http://localhost:5000/login'
session = dict()
db = dict()

@app.route("/")
def send_token():
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN,
        CONSUMER_SECRET,
        CALLBACK_URL)

    try:

        redirect_url= auth.get_authorization_url()
        session['request_token']= (auth.request_token.key,
                                   auth.request_token.secret)
    except tweepy.TweepError:
        print 'Error! Failed to get request token'

    return flask.redirect(redirect_url)

@app.route("/login")
def get_verification():

    #get the verifier key from the request url
    verifier= request.args['oauth_verifier']

    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    token = session['request_token']
    del session['request_token']

    auth.set_request_token(token[0], token[1])

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'

    api = tweepy.API(auth)

    db['api']=api
    db['access_token_key']=auth.access_token.key
    db['access_token_secret']=auth.access_token.secret
    return flask.redirect(flask.url_for('tweet'))

@app.route("/tweet")
def tweet():
    retTuple = []
    #category=['Sports','Finance','Entertainment','Technology']
    api = db['api']
    testf = codecs.open('../flatfiles/test.txt','w+',encoding='UTF-8')
    for tweet in Cursor(api.home_timeline).items(limit=5):
         if not tweet.user.screen_name=='TwistClassifier':
            testf.write(tweet.text + "\n")
    testf.seek(0)
    retTuple = classify()
    print retTuple

    return flask.render_template('index.html', tweets = retTuple)

@app.route("/classify", methods=['GET','POST'])
def classify():
    labels =[]
    #sampletext = request.form.get('txt1')

    wordId,tweetId=tp.process(2)
    #TF-IDF
    docwords,docCatIds=svmp.cacheTweetsInList(wordId,tweetId,2)
    #SVM Processing
    #1. Create libSVM file
    svmp.createTestFile(docwords,docCatIds,tweetId)
    #2. Train the SVM
    #svmp.trainLibLinear()
    labels = svmp.testSVM(1)
    #clean_dict(start_pos,end_pos)
    return labels


if __name__ == "__main__":
    app.run()
    #svmp.svmOutput()