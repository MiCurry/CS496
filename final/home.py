import re
import urllib
import json
# Convert URLS to be safe to paste into the URL redirect
from urllib import quote_plus as url_conv

import jinja2
import webapp2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        """
        self.response.write("<h1>")
        self.response.write("Hello world!")
        self.response.write("</h1>")
        """
        test = "Hello world! Soon we will be able to save tweets!"

        template_values = {
            'body': test,
        }

        template = JINJA_ENVIRONMENT.get_template("/www/index.html")
        self.response.write(template.render(template_values))


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPage),
    #webapp2.Route(r'/oath', handler=OathHandler),
    #webapp2.Route(r'/oathredir', handler=OathRedirHandler),
], debug=True)
