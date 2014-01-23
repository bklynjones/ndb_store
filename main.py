
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

DEFAULT_DEVICE = 'default_device'

class Device(ndb.Model) :
	devicename = ndb.StringProperty()
	sensormin = ndb.IntegerProperty()
	sensormax = ndb.IntegerProperty()

	

def device_key(device_name = DEFAULT_DEVICE):
	"""Constructs a  Datastore key for a SensorRecord Entity with Device name."""
	return ndb.Key('ReadRecordsHandler', device_name)

class SensorRecord(ndb.Model) :
	"""Models a single PinRead from an Arduino with record creation time,  sensor min/max, and Device name"""
	key_name = ndb.StringProperty()
	#devicename = ndb.StringProperty()
	sensorreading = ndb.IntegerProperty()
	recordentrytime = ndb.DateTimeProperty(auto_now_add=True)

	

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
       


class ReadRecordsHandler(webapp2.RequestHandler):

	def get(self): 
		self.response.headers['Content-Type'] = 'text/plain'
		
		qry = Device.query()
		self.response.write(qry)

		qry1= qry.filter(SensorRecord.key_name == 'bluto')
		self.response.write('.......................................')
		self.response.write(qry1)

        #sensor_records_query = SensorRecord.query()
        #sensor_records_results = sensor_records_query.fetch()
        #self.response.write(sensor_records_results)


app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/write', CreateRecordHandler),
	('/read', ReadRecordsHandler)
], debug=True)
 