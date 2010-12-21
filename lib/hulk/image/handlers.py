from google.appengine.ext import db
from google.appengine.ext.webapp import blobstore_handlers


class ImageUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            image = None
            key = self.request.get('key', None)
            if key is not None:
                image = db.get(db.Key(encoded=key))
            if image is not None:
                uploads = self.get_uploads()
                if len(uploads) == 1:
                    image.blob_info = uploads[0]
                    image.put()
                    self.redirect(self.get_upload_url())
                else:
                    self.error(400)
            else:
                self.error(400)
        except:
            self.error(500)

    @classmethod
    def get_upload_url(cls):
        return '/hulk/image_upload/'
