
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb


class Device(ndb.Model) :
	devicename = ndb.StringProperty()

	@classmethod
	def query_record(cls, ancestor_key):
		return cls.query(ancestor=ancestor_key).order(-cls.recordentrytime)



class SensorRecord(ndb.Model) :
# Models a single PinRead from an Arduino with record creation time,  sensor min/max, and Device name"""
	
	devicename = ndb.StringProperty()
	sensorreading = ndb.IntegerProperty()
	sensormin = ndb.IntegerProperty()
	sensormax = ndb.IntegerProperty()
	recordentrytime = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def query_record(cls, ancestor_key):
		return cls.query(ancestor=ancestor_key).order(-cls.recordentrytime)

class MainHandler(webapp2.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        
        get_values = self.request.GET
        d = Device(devicename = self.request.GET['devicename'])
        d_key = d.put()


        r = SensorRecord(parent = d_key,
        	devicename=d.devicename,
        	sensorreading = int(self.request.GET['sensorreading']),
        	sensormin = int(self.request.GET['sensormin']),
        	sensormax = int(self.request.GET['sensormax']))
        r_key= r.put()

        self.response.write(r_key.get())

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


 