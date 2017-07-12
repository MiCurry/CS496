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
class Boat(ndb.Model):
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)
    length = ndb.IntegerProperty(required=True)
    at_sea = ndb.BooleanProperty(default=True)

class BoatHandler(webapp2.RequestHandler):
    def get(self, id=None):
        if id:
            boat = ndb.Key(urlsafe=id).get()
            b_d = boat.to_dict()
            b_d['self'] = "/boat/" + id
            self.response.write(json.dumps(b_d))
        else:
            boats = Boat.query()
            for boat in boats:
                    self.response.out.write(json.dumps(boat.to_dict()))

    def post(self):
        request = json.loads(self.request.body)
        boat = Boat(name=request['name'],
                    type=request['type'],
                    length=request['length'])
        boat.at_sea = False
        boat.put()
        resp = boat.to_dict()
        resp['self'] = '/boat/' + boat.key.urlsafe()
        self.response.write(json.dumps(resp))


"""
          id - String genereated by api
      number - Slip number
current_boat - ID of the current boat, null if empty
arrival_date - String indicating the date the boat arrived in the slip,
                it should be entered by the client
"""
class Slip(ndb.Model):
    number = ndb.IntegerProperty(required=True)
    arrivial_date = ndb.StringProperty()
    current_boat = ndb.StructuredProperty(Boat)

class SlipHandler(webapp2.RequestHandler):
    def get(self, id=None):
        if id:
            slip = ndb.Key(urlsafe=id).get()
            s_d = slip.to_dict()
            s_d['self'] = "/slip/" + id
            self.response.write(json.dumps(s_d))
        else:
            slips = Slip.query()
            for slip in slips:
                    self.response.out.write(json.dumps(slip.to_dict()))

    def post(self):
        request = json.loads(self.request.body)
        slip = Slip(number=request['number'])
        slip.arrivial_date = "NULL"
        slip.current_boat = None
        slip.put()
        resp = slip.to_dict()
        resp['self'] = '/slip/' + slip.key.urlsafe()
        self.response.write(json.dumps(resp))

class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World!')

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    ('/boat', BoatHandler),
    ('/boat/(.*)', BoatHandler),
    ('/slip/', SlipHandler),
    ('/slip/(.*)', SlipHandler)
], debug=True)
