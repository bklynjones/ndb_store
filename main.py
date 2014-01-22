
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

d = Device(devicename = 'bluto')
d_key = d.put()



r = SensorRecord(parent = d_key,
				devicename=d.devicename,
				sensorreading = 3,
				sensormin = 0,
				sensormax = 10)
r_key= r.put()


class MainHandler(webapp2.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(r_key.get())
       # self.response.write(d.query_record)






app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
