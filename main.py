
import urllib
import webapp2

try: import simplejson as json
except ImportError: import  json

from google.appengine.api import users
from google.appengine.ext import ndb
from urlparse import urlparse, parse_qs

from datetime import datetime

import ast

from itertools import izip


NO_DEVICE_NAMED = 'no_device_name'

def device_key(device_name = NO_DEVICE_NAMED):
	"""constructs Datastore key for SensorRecord entity with device_name """
	return ndb.Key('DeviceGroup', device_name)


class SensorRecord(ndb.Model) :
	"""Models a single PinRead from an Arduino with record creation time,  sensor min/max, and Device name"""
	sensorreading= ndb.JsonProperty(indexed = True, compressed = False)
	recordentrytime = ndb.DateTimeProperty(auto_now_add=True)

	#note: all class methods pass the instance of the class as it's first argument 
	@classmethod
	def query_readings_by_device(cls,device_name):
			device_readings_list = []
			device_records_query = cls.query(
			ancestor = device_key(device_name),
			projection = [SensorRecord.recordentrytime, SensorRecord.sensorreading]).order(-SensorRecord.recordentrytime)
			# device_records is a list object only returns sensor reading and time for parsing. 
			device_records = device_records_query.fetch()
			return device_records


	@classmethod
	def query_readings_by_device_with_timestamp(cls,device_name):
			device_readings_dict = {}
			device_records_query = cls.query(
			ancestor = device_key(device_name)).order(-SensorRecord.recordentrytime)
			
			device_records = device_records_query.fetch()

			
			return device_records

	@classmethod
	def query_latest_reading(cls,device_name):
		
		device_records_query = cls.query(
			ancestor = device_key(device_name)).order(-SensorRecord.recordentrytime)
			# device_records is a list object only returns sensor reading and time for parsing. 
		device_record = device_records_query.fetch(1)
		return device_record[0].sensorreading

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('hello world')

class CreateRecordHandler(webapp2.RequestHandler):
    
    def get(self):

    	
    	# populates datastore Model Objects with GET Params and creates Datastore Entity
        self.response.headers['Content-Type'] = 'text/plain'
        #the following request objects are used to collect the arguments from the Query string (everything after the '?')
        device_name = self.request.GET['devicename']
        
        r = SensorRecord(parent = device_key(device_name),
        				sensorreading = json.dumps(self.request.GET.items(), separators=(',', ':')))
        				
        r_key = r.put()



class ReadRecordsHandler(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
		
		try:
			device_name= self.request.GET['devicename']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			sensor_readings = SensorRecord.query_readings_by_device(device_name)

			self.response.write('{ "%s":{"readings":'%(device_name))
			for sensor_reading in sensor_readings:
				entry_time = sensor_reading.recordentrytime.strftime("%a,%b,%d,%H,%M,%S")
				sensor_vals = ast.literal_eval(sensor_reading.sensorreading)
				self.response.write('"%s":'%entry_time)
		 		for i in range(1, len(sensor_vals)):
		 			self.response.write('{')
		 			
					self.response.write('"%s":'%(sensor_vals[i][0]))
					self.response.write('"%s"'%(sensor_vals[i][1]))
					self.response.write('}')
					if i < (len(sensor_vals)-1):
						self.response.write(',')
			self.response.write('}')


			# 	self.response.write('"datetime":"%s",{'%(entry_time))
			# 	for key, value in sensor_vals.iteritems():
			# 		self.response.write('%s:%s,'%(key, value))
			# self.response.write(type(sensor_vals))	
			# self.response.write('}}')
			#self.response.write(dir(sensor_vals))











class ReadRecordsHandlerWithTime(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
		
		try:
			device_name= self.request.GET['devicename']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			self.response.write(
			SensorRecord.query_readings_by_device_with_timestamp(device_name))

class ReadLatestRecordHandler(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
		
		try:
			device_name= self.request.GET['devicename']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:

			reading = SensorRecord.query_latest_reading(device_name)
			


			#self.response.write(decoded_dict.get('devicename') + '\n')
			#self.response.write(decoded_dict.get('a0'))

			self.response.write(reading)

		
			 #outputs key value dictionary of retrieved datastore entity. 
		
			

class PassSensorValueOnly(webapp2.RequestHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'

		try:
			device_name= self.request.GET['devicename']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			reading = SensorRecord.query_latest_reading(device_name)
			decoded_dict = dict(json.loads(reading))
			self.response.write(decoded_dict.get('a0'))


app = webapp2.WSGIApplication([
	webapp2.Route('/', handler = MainHandler, name = 'home'),
	webapp2.Route('/write', handler =  CreateRecordHandler, name = 'create-record'),
	webapp2.Route('/read', handler = ReadRecordsHandler, name = 'read-values'),
	webapp2.Route('/read-time', handler = ReadRecordsHandlerWithTime, name = 'read-values-with-time'),
	webapp2.Route('/read-latest', handler = ReadLatestRecordHandler, name = 'read-latest-value'),
	webapp2.Route('/a0', handler = PassSensorValueOnly, name = 'pass-sensor-value-a0')

], debug=True)


 