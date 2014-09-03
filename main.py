import os
import urllib
import webapp2

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
import StringIO



#This model is needed to retrieve ALL records for a particular device. This will be hardcoded now but eventually pulled from POST header
default_device_val = 'no_device_name'
def device_key(device_name = default_device_val):
  """constructs Datastore key for BlobRecorder entity with device_name """
  return ndb.Key('DeviceGroup', device_name)


""" This model is keeps track of the keys of uploaded blobs and the time of upload."""

class BlobRecorder(ndb.Model):
    ##This is a 'custom' property that is specifically for referencing Blobstore objects
    device_name = ndb.StringProperty()
    blob_file_key = ndb.BlobKeyProperty()
    recordentrytime = ndb.DateTimeProperty(
    auto_now_add=True)


    """Returns a list of blobs, the second arguement 
    limits the number of records returned in the query and sorts them in  first in last out order"""
    @classmethod
    def query_blobs_by_device(cls,device_name, number_of_entries_to_fetch=0):

      output_buffer = StringIO.StringIO()
      
      ## Return a list of blob refence keys for the given device
      blob_list_query = cls.query(
        ancestor = device_key(device_name),
        projection = [BlobRecorder.recordentrytime, BlobRecorder.blob_file_key]).order(-BlobRecorder.recordentrytime)
      ## If no argument is submitted in method parameter return all entries. 
      if number_of_entries_to_fetch == 0:
          blob_list_records = blob_list_query.fetch()
      else: blob_list_records = blob_list_query.fetch(number_of_entries_to_fetch)

      #Loop through values and format time from UTC to human parsable. 
      for blob_list_record in blob_list_records:
        entry_time = blob_list_record.recordentrytime #.strftime("%a,%b,%d,%H,%M,%S")
        output_buffer.write('{"datetime" :"%s",'%entry_time)
        output_buffer.write('{"blobfile" :"%s",'%str(blob_list_record.blob_file_key))

      return output_buffer.getvalue()
      

## for Debug this presents a form for uploading the file.   This POST will be made via node. 
class MainHandler(webapp2.RequestHandler):
    def get(self):
      upload_url = blobstore.create_upload_url('/upload')
      self.response.out.write('<html><body><form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
      self.response.out.write("""Upload File: <input type="file" name="file">
        <br><input type="submit" name="submit" value="Submit"><br> 
        </form></body></html>""")

## This upload handler is trigged on POST from MainHandler
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
 
    def post(self):

   
      # 'file' is file upload field in the form
      upload_files = self.get_uploads('file')  
      # first (and only) file item in the 
      blob_info = upload_files[0]

      #store BlobKey 
      # https://developers.google.com/appengine/docs/python/blobstore/blobkeyclass
      b = BlobRecorder(parent = device_key(device_name = 'stan'),
                      blob_file_key = blob_info.key() )
      b_key = b.put()

      #redirect to serve page which downloads blob using the resource from the parameter in the GET string
      
      self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    #pull in key string from URL 
    resource = str(urllib.unquote(resource))
    #retrieve BlobInfo Entity by passing key refernence to .get()
    blob_info = blobstore.BlobInfo.get(resource)
    self.response.write(blob_info)
    #This blob store handler method sends the blob as a response. 
    self.send_blob(blob_info)


class RetrieveRecordsHandler(webapp2.RequestHandler):
  def get(self):

    this = self
    
    self.response.headers['Access-Control-Allow-Origin'] = '*'

    try:
      device_name= self.request.GET['devicename']

    except KeyError: #bail if there is no argument for 'devicename' submitted
      self.response.write ('NO DEVICE_NAME PARAMETER SUBMITTED')

    else:
      blob_reference_keys = BlobRecorder.query_blobs_by_device(device_name)
      #Output Query
      self.response.write(blob_reference_keys)
    




app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/upload', UploadHandler),
                               ('/serve/([^/]+)?', ServeHandler),
                               ('/rr', RetrieveRecordsHandler)],
                              debug=True)