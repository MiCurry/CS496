import re
import urllib
import json
# Convert URLS to be safe to paste into the URL redirect
from urllib import quote_plus as url_conv

from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import webapp2

EXCHANGE_URL = "https://www.googleapis.com/oauth2/v4/token"
GOOGLE_PLUS_SCOPE_URL = "https://www.googleapis.com/auth/userinfo.profile"
OATH_REDIRECT_URL = "http://oath-auth.appspot.com/oathredir"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth?scope="
WELCOME_REDIRECT_URL = "http://oath-auth.appspot.com/welcome"

client = json.load(open('client_id.json'))
client_id = client['web']['client_id']
client_secret = client['web']['client_secret']

class OathHandler(webapp2.RequestHandler):
    def get(self):
        redirect_uri = url_conv(OATH_REDIRECT_URL)
        scope = url_conv(GOOGLE_PLUS_SCOPE_URL)

        auth_uri = GOOGLE_AUTH_URL+scope+\
                   "&redirect_uri="+redirect_uri+\
                   "&response_type=code&client_id="+client_id\

        self.redirect(str(auth_uri))

class OathRedirHandler(webapp2.RequestHandler):
    def get(self):
        url = self.request.url
        auth_code = url.split("=")[1]

        payload = { 'grant_type': 'authorization_code',
                    'code': auth_code,
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': WELCOME_REDIRECT_URL,}

        payload = urllib.urlencode(payload)
        result = urlfetch.fetch(url=EXCHANGE_URL, payload = payload, method=urlfetch.POST)
        self.redirect('/welcome')

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome!")

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello world!")


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPage),
    webapp2.Route(r'/oath', handler=OathHandler),
    webapp2.Route(r'/oathredir', handler=OathRedirHandler),
    webapp2.Route(r'/welcome', handler=WelcomeHandler)
], debug=True)
