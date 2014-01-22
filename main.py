
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb


class Device(ndb.Model) :
	devicename = ndb.StringProperty()
	sensormin = ndb.IntegerProperty()
	sensormax = ndb.IntegerProperty()

	@classmethod
	def query_device(cls, ancestor_key):
		return cls.query().order(-cls.recordentrytime)



class SensorRecord(ndb.Model) :
# Models a single PinRead from an Arduino with record creation time,  sensor min/max, and Device name"""
	
	key_name = ndb.StringProperty()
	#devicename = ndb.StringProperty()
	sensorreading = ndb.IntegerProperty()
	recordentrytime = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def query_record(cls, ancestor_key):
		return cls.query(ancestor=ancestor_key).order(-cls.recordentrytime)

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('hello world')

class CreateRecordHandler(webapp2.RequestHandler):
    
    def get(self):
    	# populates datastore Model Objects with GET Params and creates Datastore Entity
        self.response.headers['Content-Type'] = 'text/plain'
        
        get_values = self.request.GET
        d = Device(devicename = self.request.GET['devicename'],
        	sensormin = int(self.request.GET['sensormin']),
        	sensormax = int(self.request.GET['sensormax']))
        d_key = d.put()

        r = SensorRecord(parent = d_key,
        	key_name=d.devicename,
        	sensorreading = int(self.request.GET['sensorreading']))
        r_key= r.put()
        r = r_key.get
        #self.response.write(r)
        d = d_key.get()
        self.response.write(d)
        sensor_records_query = SensorRecord.query()
        sensor_records_results = sensor_records_query.fetch()
        self.response.write(sensor_records_results)

app = webapp2.WSGIApplication([
	('/', MainHandler),
    ('/write', CreateRecordHandler)
], debug=True)


 