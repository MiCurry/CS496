import json
import tweepy

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import jinja2
import webapp2

access_token =  "898320587562471424-OFtFHkf8U950LX4Q3gzETxHuZT5mS87"
access_token_secret =  "jsJR4tPv5hyIGDVGW7RF1XDcOAK8bTVkMD1W4SZPeP7AR"
consumer_key = "DeeH4LEeZzqnBn4U0LVglmY00"
consumer_secret = "yOX3dcgyS5VGLgX6Dy7Qo1zAcoa65eSjEC0xGa2qQuL5zzKMTy"
twetTweetTweeet = "https://twitter.com/TwetTweetTweeet/status/"

class Tweet(ndb.Model):
    tweet_id  = ndb.StringProperty(required=True) # Twitter Person who tweeter the tweet
    tweet_sender = ndb.StringProperty(required=True) # User who saved the tweet
    body = ndb.StringProperty(required=True)
    date_tweeted = ndb.StringProperty(required=True)
    url = ndb.StringProperty(required=True)

def tweepy_init():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

class TweetHandler(webapp2.RequestHandler):
    def get(self, user_id=None, tweet_id=None):
        self.response.content_type='application/json'
        if tweet_id: # Get a specific tweet
            tweet = Tweet.query(Tweet.tweet_id == tweet_id).get()
            if tweet:
                t_d = tweet.to_dict()
                t_d['self'] = tweet_id
                self.response.status_int=200
                self.response.write(json.dumps(t_d))
                return
            else:
                self.response.status_int=404
                self.response.write("")
                return
        elif user_id: # List Tweets from a specific User
            user = ndb.Key(urlsafe=user_id).get()
            if user:
                resp = []
                for t in user.tweets:
                    tweet = Tweet.query(Tweet.tweet_id == t.tweet_id).get()
                    resp.append(tweet.to_dict())

                self.response.status_int = 200
                self.response.write(json.dumps(resp))
                return
            else: # User Not Found
                self.response.status_int = 404
                self.response.out.write("")
                return
        # List all tweets
        tweets = Tweet.query()
        resp = []
        for tweet in tweets:
            resp.append(tweet.to_dict())

        self.response.status_int = 200
        self.response.out.write(json.dumps(resp))
        return

    def post(self, user_id=None):
        request = json.loads(self.request.body)
        header = self.request.headers

        """ Check Oauth Token """
        token = header['token']

        headers = {'Authorization': 'Bearer {}'.format(token)}
        req_uri = 'https://www.googleapis.com/plus/v1/people/me'
        r = urlfetch.fetch(url = req_uri,
                           headers = headers,
                           method = urlfetch.GET)

        r = json.loads(r.content)
        if 'error' in r:
            self.response.status_int = 401
            self.response.status_message="Bad Access Token!"
            self.response.write("BAD ACCESS TOKEN")
            return

        """ Token Good! Continue! """
        body = request['body']
        if not body:
            self.response.status_int = 400
            self.response.out.write("")
            return
        if not user_id:
            self.response.status_int = 400
            self.response.out.write("")
            return
        else:
            user = ndb.Key(urlsafe=user_id).get()

        api = tweepy_init() # Init tweepy
        try:
            status = api.update_status(body) # Update Status (AKA Tweet)
        except Exception as e:
            self.response.status_int = 400
            self.response.out.write("")
            return

        tweet = Tweet(tweet_id=str(status.id),
                        tweet_sender=user.userName,
                        body=status.text,
                        date_tweeted=str(status.created_at),
                        url=twetTweetTweeet + str(status.id)
                        )

        tweet.put()
        user.tweets.append(tweet)
        user.put()
        self.response.status_int = 200
        self.response.out.write(json.dumps(tweet.to_dict()))
        return
