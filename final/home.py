import os
import re
import urllib
import json
# Convert URLS to be safe to paste into the URL redirect
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import urlfetch
from urllib import quote_plus as url_conv

import jinja2
import webapp2

from oath2 import OathHandler, OathRedirHandler, checkToken
from twitter import TweetHandler

GOOGLE_USER_INFO_REQ_URI = "https://www.googleapis.com/plus/v1/people/me"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Profile(ndb.Model):
    userName = ndb.StringProperty(required=True)
    gplusID = ndb.StringProperty(required=True)
    firstName = ndb.StringProperty(required=True)
    favColor = ndb.StringProperty()
    location = ndb.StringProperty()
    tweets = ndb.KeyProperty(repeated=True)

class Tweet(ndb.Model):
    tweet_author = ndb.StringProperty(required=True) # Twitter Person who tweeter the tweet
    tweet_saver = ndb.KeyProperty(required=True) # User who saved the tweet
    body = ndb.StringProperty(required=True)
    date_tweeted = ndb.StringProperty(required=True)
    date_saved = ndb.StringProperty(required=True)

class ProfileHandler(webapp2.RequestHandler):
    def get(self, user_id=None):
        self.response.content_type='application/json'
        if user_id: # List Single User
            user = ndb.Key(urlsafe=user_id).get()
            if user:
                u_d = user.to_dict()
                u_d['self'] = "/profile/" + user_id
                self.response.write(json.dumps(u_d))
                return
            else:
                self.response.status_int = 404
                self.response.out.write("")
                return

        # List all Users
        users = Profile.query()
        resp = []
        for user in users:
            resp.append(user.to_dict())

        self.response.status_int = 200
        self.response.out.write(json.dumps(resp))
        return

    def post(self):
        self.response.content_type='application/json'
        request = json.loads(self.request.body)
        header = self.request.headers

        token = header['token']

        headers = {'Authorization': 'Bearer {}'.format(token)}
        req_uri = 'https://www.googleapis.com/plus/v1/people/me'
        r = urlfetch.fetch(url = req_uri,
                           headers = headers,
                           method = urlfetch.GET)

        r = json.loads(r.content)
        if 'error' in r:
            self.response.status_int = 403
            self.response.status_message="Bad Access Token!"
            self.response.write("BAD ACCESS TOKEN")
            return

        firstName = r['name']['givenName']
        userID = r['id']
        userName = request['userName']
        color = request['color']
        loc = request['location']

        user = Profile(userName=userName,
                        firstName=firstName,
                        gplusID=userID,
                        favColor=color,
                        location=loc)

        user.put()
        resp = user.to_dict()
        resp['self'] = user.key.urlsafe()

        self.response.status_int = 201
        self.response.write(json.dumps(resp))

    def patch(self, user_id=None):
        self.response.content_type='application/json'
        request = json.loads(self.request.body)
        user = ndb.Key(urlsafe=str(user_id)).get()
        if not user:
            self.response.status_int=404
            self.response.status_message="Boat Not Found"
            self.response.out.write("")

        if 'location' in request:
            user.location = request['location']
        if 'color' in request:
            user.favColor = request['color']

        user.put()
        resp = user.to_dict()
        resp['self'] = user.key.urlsafe()
        self.response.status_int = 200
        self.response.write(json.dumps(resp))

    def delete(self, user_id=None):
        self.response.content_type='application/json'
        user = ndb.Key(urlsafe=user_id).get()
        if user:
            u_k = user.key
            u_k.delete()
            self.response.status_int = 204
            self.response.out.write("")
        else:
            self.response.status_int = 503
            self.response.out.write("")

class MainPage(webapp2.RequestHandler):
    def get(self):
        out = "Hello world! Soon we will be able to save tweets!"

        template_values = {
            'body': out,
        }

        template = JINJA_ENVIRONMENT.get_template("/www/index.html")
        self.response.write(template.render(template_values))
        self.response.status_int = 200


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPage),
    webapp2.Route(r'/index.html', handler=MainPage),
    webapp2.Route(r'/profile.html', handler=ProfileHandler),
    webapp2.Route(r'/profile', handler=ProfileHandler),
    webapp2.Route(r'/profile/<user_id>', handler=ProfileHandler),
    webapp2.Route(r'/oath', handler=OathHandler),
    webapp2.Route(r'/oathredir', handler=OathRedirHandler),
    webapp2.Route(r'/tweet', handler=TweetHandler)
], debug=True)
