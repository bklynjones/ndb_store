import os
import urllib
import webapp2

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
import StringIO




class BlobRecorder(ndb.Model):

    blob_file_key = ndb.BlobKeyProperty()
    recordentrytime = ndb.DateTimeProperty(
    auto_now_add=True)

    @classmethod
    def query_list_of_blobs(cls,number_of_entries_to_fetch=0):

      output_buffer = StringIO.StringIO()
      
      ## Return a list of blob refence keys for given device
      blobs_query = cls.query().order(-BlobRecorder.recordentrytime)

      if number_of_entries_to_fetch == 0:
          blob_key_records = blobs_query.fetch()
      else: blobs_query = blobs_query.fetch(number_of_entries_to_fetch)

      for blob_key_record in blob_key_records:
        entry_time = blob_key_record.recordentrytime #.strftime("%a,%b,%d,%H,%M,%S")
        
        output_buffer.write('{"datetime" :"%s",'%entry_time)
        output_buffer.write('{"blobfile" :"%s",'%blob_key_record.blob_file_key)

class MainHandler(webapp2.RequestHandler):
    def get(self):
      upload_url = blobstore.create_upload_url('/upload')
      self.response.out.write('<html><body><form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
      self.response.out.write("""Upload File: <input type="file" name="file">
        <br><input type="submit" name="submit" value="Submit"><br> 
        </form></body></html>""")


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
 
      

    def post(self):
      
      upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
      blob_info = upload_files[0]
  
      b = BlobRecorder(blob_file_key = blob_info.key())
      b_key = b.put()


      self.response.out.write('/serve/%s' % blob_info.key())
      self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.response.write(blob_info)
    self.send_blob(blob_info)

class RetrieveHandler(blobstore_handlers.BlobstoreDownloadHandler):
     def get(self):


        # resource = str(urllib.unquote(resource))
        # blob_info = blobstore.BlobInfo.get(resource)
        # self.send_blob(blob_info)
        blobs = blobstore.BlobInfo.get(blob_keys);

        for blob in blobs :
            self.response.write(blob)

class RetrieveRecordsHandler(webapp2.RequestHandler):
  def get(self):

    this = self
    
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    blob_reference_keys = BlobRecorder.query_list_of_blobs()
    self.response.write(blob_reference_keys)
    




app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/upload', UploadHandler),
                               ('/serve/([^/]+)?', ServeHandler),
                               ('/retrieve', RetrieveHandler),
                               ('/rr', RetrieveRecordsHandler)],
                              debug=True)