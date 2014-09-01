import os
import urllib
import webapp2

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb


default_device_val = 'stanley'

def device_key(device_name = default_device_val):
    """constructs Datastore key for device uploading blob entity """
    return ndb.Key('DeviceGroup', device_name)


class BlobRecorder(ndb.Model):
    file = ndb.BlobKeyProperty()
    blob_key = blobstore.BlobReferenceProperty()

class MainHandler(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/upload')
    self.response.out.write('<html><body>')
    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
    self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
        name="submit" value="Submit"> </form></body></html>""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]

    device_name = default_device_val

    b = BlobRecorder(parent = device_key(device_name),
                    file = blob_info.key())
    b_key = b.put()


    self.redirect('/serve/%s' % blob_info.key())


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.response.write(blob_info)
    self.response.out.write('hello')

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
    records = ndb.Key('no_device_name',file)

    for record in records :
        self.response.write(record)



app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/upload', UploadHandler),
                               ('/serve/([^/]+)?', ServeHandler),
                               ('/retrieve', RetrieveHandler),
                               ('/rr', RetrieveRecordsHandler)],
                              debug=True)