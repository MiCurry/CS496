import re
import datetime

from google.appengine.ext import ndb
import webapp2
import json

class Boat(ndb.Model):
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)
    length = ndb.IntegerProperty(required=True)
    at_sea = ndb.BooleanProperty(default=True)

class Slip(ndb.Model):
    number = ndb.IntegerProperty(required=True)
    arrival_date = ndb.StringProperty()
    current_boat = ndb.StringProperty()



class BoatHandler(webapp2.RequestHandler):

    def get(self, boat_id=None):
        self.response.content_type='application/json'
        if boat_id:
            boat = ndb.Key(urlsafe=boat_id).get()
            b_d = boat.to_dict()
            b_d['self'] = "/boats/" + boat_id
            self.response.write(json.dumps(b_d))
        else:
            boats = Boat.query()
            resp = []
            for boat in boats:
                resp.append(boat.to_dict())

            self.response.status_int = 200
            self.response.out.write(json.dumps(resp))

    def post(self):
        self.response.content_type='application/json'
        request = json.loads(self.request.body)

        boat = Boat(name=request['name'],
                    type=request['type'],
                    length=request['length'])
        boat.put()
        resp = boat.to_dict()
        resp['self'] = '/boats/' + boat.key.urlsafe()

        self.response.status_int = 201
        self.response.write(json.dumps(resp))

    def patch(self, boat_id=None):
        self.response.content_type='application/json'
        request = json.loads(self.request.body)
        boat = ndb.Key(urlsafe=boat_id).get()
        if not boat:
            self.response.status_int=404
            self.response.status_message="Boat Not Found"
            self.response.out.write("")
        if 'name' in request:
            boat.name = request['name']
        if 'type' in request:
            boat.type = request['type']
        if 'length' in request:
            boat.length = request['length']

        boat.put()
        resp = boat.to_dict()
        resp['self'] = '/boats/' + boat.key.urlsafe()
        self.response.status_int = 200
        self.response.write(json.dumps(resp))

    def delete(self, boat_id=None):
        self.response.content_type='application/json'
        boat = ndb.Key(urlsafe=boat_id).get()
        if boat:
            b_k = boat.key
            b_k.delete()
            self.response.status_int = 204
            self.response.out.write("")
        else:
            self.response.status_int = 503
            self.response.out.write("")

class SlipHandler(webapp2.RequestHandler):
    def get(self, slip_id=None):
        self.response.content_type='application/json'
        print "GET!"
        if slip_id: # Get Single Slip
            slip = ndb.Key(urlsafe=slip_id).get()
            s_d = slip.to_dict()
            s_d['self'] = "/slips/" + slip_id
            self.response.write(json.dumps(s_d))
        else:
            slips = Slip.query()
            resp = []
            for slip in slips:
                resp.append(slip.to_dict())
            self.response.status_int = 200
            self.response.out.write(json.dumps(resp))

    def post(self):
        request = json.loads(self.request.body)
        slip = Slip(number=request['number'])
        slip.arrivial_date = "NULL"
        slip.current_boat = None
        slip.put()
        resp = slip.to_dict()
        resp['self'] = '/slips/' + slip.key.urlsafe()

        self.response.status_int = 201
        self.response.status = "201 Created"
        self.response.write(json.dumps(resp))

    def patch(self, slip_id=None):
        self.response.content_type='application/json'
        request = json.loads(self.request.body)
        slip = ndb.Key(urlsafe=slip_id).get()

        if not slip:
            self.response.status_int=404
            self.response.status_message="Slip Not Found"
            self.response.out.write("")
        else:
            if 'number' in request:
                slip.number = request['number']
            slip.put()
            resp = slip.to_dict()
            resp['self'] = '/slips/' + slip.key.urlsafe()
            self.response.status_int = 200
            self.response.write(json.dumps(resp))

    def delete(self, slip_id=None):
        self.response.content_type='application/json'
        slip = ndb.Key(urlsafe=slip_id).get()
        if slip:
            s_k = slip.key
            s_k.delete()
            self.response.status_int = 204
            self.response.status_message = "Status: 204 No Content"
            self.response.out.write("")
        else:
            self.response.status_int = 503
            self.response.out.write("")


class DockHandler(webapp2.RequestHandler):
    """ Get Boat docked at slip """
    def get(self, slip_id=None):
        self.response.content_type='application/json'
        resp = []

        slip = ndb.Key(urlsafe=slip_id).get()
        if not slip: # To see if slip exists or not
            self.response.status_int=404
            self.response.status_message="Slip Not Found"
            self.response.out.write("")
        else:
            if not slip.current_boat: # To see if there is a boat present
                self.response.status_int=404
                self.response.out.write("")
            else: # Respond with slip if boat is present
                self.response.status_int=200
                self.response.out.write(json.dumps(slip.to_dict()))

    def put(self, slip_id=None, boat_id=None, name=None):
        """ Docking a boat """
        self.response.content_type='application/json'
        resp = []

        slip = ndb.Key(urlsafe=slip_id).get()
        boat_id = re.sub("/boats/", '', str(boat_id))
        boat = ndb.Key(urlsafe=boat_id).get()
        if not slip: # Check to see if slip exists
            self.response.status_int=404
            self.response.status_message="Slip Not Found"
            self.response.out.write("")
        elif not boat: # Check to see if boat exists
            self.response.status_int=404
            self.response.status_message="Boat Not Found"
            self.response.out.write("")
        elif slip.current_boat: # Slip contains a boat so we can't put a new boat
            self.response.status_int=403
            self.response.status_message="Slip occupied"
            self.response.out.write("")
        else: # Slip Empty! So we can mark slip and boat properties
            slip.current_boat = "/boats/" + boat.key.urlsafe()
            today = datetime.date.today()
            slip.arrival_date = today.strftime("%b-%m-%Y")
            boat.at_sea = False
            slip.put(); boat.put()
            self.response.status_int=201
            self.response.out.write(json.dumps(slip.to_dict()))

    def delete(self, slip_id=None):
        self.response.content_type='application/json'

        slip = ndb.Key(urlsafe=slip_id).get()
        boat_id = re.sub("/boats/", '', str(slip.current_boat))
        boat = ndb.Key(urlsafe=boat_id).get()
        if not slip:
            self.response.status_int=404
            self.response.status_message="Slip Not Found"
            self.response.out.write("")
        elif not slip.current_boat:
            self.response.status_int=503
            self.response.out.write("")
        else:
            slip.current_boat = None
            slip.arrival_date = "NULL"
            boat.at_sea = True
            slip.put(); boat.put()
            self.response.status_int=204
            self.response.out.write("")

class AtSeaHandler(webapp2.RequestHandler):
    def put(self, boat_id=None):
        boat = ndb.Key(urlsafe=boat_id).get()
        if not boat: # If Boat doesn't exist
            self.response.status_int=404
            self.response.status_message="Boat Not Found"
            self.response.out.write("Boat Not Found")
        elif boat.at_sea == True: # If Boat is already at sea
            self.response.status_int=403
            self.response.out.write("Boat Already at Sea")
        else:
            slip = Slip.query(Slip.current_boat == '/boats/' + boat_id).get()
            slip.current_boat = None
            slip.arrival_date = None
            boat.at_sea = True
            boat.put(); slip.put()
            self.response.status_int = 204


class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World!')

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=HelloWebapp2),
    webapp2.Route(r'/boats', handler=BoatHandler),
    webapp2.Route(r'/boats/<boat_id>', handler=BoatHandler),
    webapp2.Route(r'/slips', handler=SlipHandler),
    webapp2.Route(r'/slips/<slip_id>', handler=SlipHandler),
    webapp2.Route(r'/slips/<slip_id>/dock', handler=DockHandler, name='dock'),
    webapp2.Route(r'/slips/<slip_id>/dock/boats/<boat_id>', handler=DockHandler, name='dock'),
    webapp2.Route(r'/boats/<boat_id>/atsea', handler=AtSeaHandler),
], debug=True)
