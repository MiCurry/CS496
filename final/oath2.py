import os
import re
import urllib
import json
# Convert URLS to be safe to paste into the URL redirect
from urllib import quote_plus as url_conv

from google.appengine.api import urlfetch
from google.appengine.api import memcache

import jinja2
import webapp2

from shared import state_generator

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

EXCHANGE_URL = "https://www.googleapis.com/oauth2/v4/token"
GOOGLE_PLUS_SCOPE_URL = "https://www.googleapis.com/auth/userinfo.profile"
OATH_REDIRECT_URL = "http://tweet-saver.appspot.com/oathredir"
OATH_URL = "http://tweet-saver.appspot.com/oath"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth?scope="
PROFILE_REDIRECT_URL = "http://tweet-saver.appspot.com/profile"
GIF_LINK = "http://i.imgur.com/GVKjxsP.gif"
TOKEN_INFO = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="

client = json.load(open('client_id.json'))
client_id = client['web']['client_id']
client_secret = client['web']['client_secret']

ACCESS_TOKEN = None

my_state = state_generator()
memcache.add(key='state', value=my_state, time=3600)

def checkToken(token):
    url = TOKEN_INFO + token
    result = urlfetch.fetch(url=url)
    return result

class OathHandler(webapp2.RequestHandler):
    def get(self):
        redirect_uri = url_conv(OATH_REDIRECT_URL)
        scope = url_conv(GOOGLE_PLUS_SCOPE_URL)

        auth_uri = GOOGLE_AUTH_URL+scope+\
                   "&redirect_uri="+redirect_uri+\
                   "&response_type=code&client_id="+client_id+\
                   "&state="+memcache.get(key='state')\

        self.redirect(str(auth_uri))

class OathRedirHandler(webapp2.RequestHandler):
    def get(self):
        url = self.request.url
        expected_state = memcache.get(key='state')
        state = url.split("=")[1]
        auth_code = url.split("=")[2]

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = { 'grant_type': 'authorization_code',
                    'code': auth_code,
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': OATH_REDIRECT_URL,}


        payload = urllib.urlencode(payload)

        result = urlfetch.fetch(url=EXCHANGE_URL,
                                payload = payload,
                                method=urlfetch.POST,
                                headers=headers)

        result = json.loads(result.content)
        ACCESS_TOKEN = result['access_token']
        headers = {'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)}
        req_uri = 'https://www.googleapis.com/plus/v1/people/me'
        r = urlfetch.fetch(url = req_uri,
                           headers = headers,
                           method = urlfetch.GET)

        r = json.loads(r.content)
        givenName = r['name']['givenName']
        familyName = r['name']['familyName']
        user_google_plus_url = r['url']

        result = checkToken(ACCESS_TOKEN)
        result2 = checkToken("BAAHH")

        template_values = {
            'first': str(givenName),
            'token': str(ACCESS_TOKEN),
        }

        template = JINJA_ENVIRONMENT.get_template("/www/profile.html")
        self.response.write(template.render(template_values))
