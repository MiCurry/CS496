from google.appengine.ext import ndb
import webapp2
import json


""" class boat(ndb.model)
    id - "abc123" - Should be automatically generated - String
  name - "Sea Witch" - The name of the boat - string
  type - "Catamaran" - Type of boat - String
          > Power Boat
          > Sailboat
          > catamaran
          > etc
length - 28 # Length of the boat - Intiger
at_sea - false # True of false representing at sea or not
"""
class boat(ndb.Model):

class BoatHandler(webapp2.RequestHandler):
    def get(self):
        self.request.body

    def post(self):
        boat_data = json.loads(self.requst.body)
        self.response.write(json.dumps(boat_data))

"""
          id - String genereated by api
      number - Slip number
current_boat - ID of the current boat, null if empty
arrival_date - String indicating the date the boat arrived in the slip,
                it should be entered by the client
"""
class slip(ndb.Model):
    pass

class SlipHandler(webapp2.RequestHandler):
    def get(self):
        self.request.body

    def post(self):
        boat_data = json.loads(self.request.body)
        self.response.write(json.dumps(boat_data))

class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World!')

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    ('/boat', BoatHandler),
    ('/boat/slip', SlipHandler)
], debug=True)
