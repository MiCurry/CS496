import os
import re
import urllib
import json
# Convert URLS to be safe to paste into the URL redirect
from google.appengine.ext import ndb
from urllib import quote_plus as url_conv

import jinja2
import webapp2

from oath2 import OathHandler, OathRedirHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Profile(ndb.Model):
    userName = ndb.StringProperty(required=True)
    favColor = ndb.StringProperty()
    location = ndb.StringProperty()
    tweets = ndb.KeyProperty(repeated=True)

class Tweet(ndb.Model):
    tweet_author = ndb.StringProperty(required=True) # Twitter Person who tweeter the tweet
    tweet_saver = ndb.KeyProperty(required=True) # User who saved the tweet
    body = ndb.StringProperty(required=True)
    date_tweeted = ndb.StringProperty(required=True)
    date_saved = ndb.StringProperty(required=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        out = "Hello world! Soon we will be able to save tweets!"

        template_values = {
            'body': out,
        }

        template = JINJA_ENVIRONMENT.get_template("/www/index.html")
        self.response.write(template.render(template_values))


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPage),
    webapp2.Route(r'/oath', handler=OathHandler),
    webapp2.Route(r'/oathredir', handler=OathRedirHandler),
], debug=True)
