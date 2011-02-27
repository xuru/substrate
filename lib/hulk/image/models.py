from cStringIO import StringIO
import urllib2
import urlparse

from google.appengine.api import images
from google.appengine.ext import db, blobstore

from urllib2_file import UploadFile


class Image(db.Model):
    blob_info = blobstore.BlobReferenceProperty(required=False, default=None)
    source_url = db.StringProperty(required=False, default=None)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

    @property
    def blob_key(self):
        key = None
        if self.blob_info is not None:
            key = self.blob_info.key()
        return key

    @property
    def image(self):
        image = None
        if self.blob_key is not None:
            image = images.Image(blob_key=self.blob_key)
        return image

    @property
    def image_data(self):
        data = None
        if self.blob_key is not None:
            data = blobstore.BlobReader(self.blob_key).read()
        return data

    def get_serving_url(self, *args, **kwargs):
        return images.get_serving_url(self.blob_key, *args, **kwargs)

    @classmethod
    def create_new_entity(cls, **kwargs):
        image = cls(**kwargs)
        image.put()
        return image

    @classmethod
    def create(cls, data=None, filename=None, url=None, upload_url=None, handler=None, **kwargs):
        if data is None:
            if url is not None:
                data = StringIO(urllib2.urlopen(url).read())
                if filename is None:
                    path = urlparse.urlsplit(url)[2]
                    filename = path[path.rfind('/')+1:]
        if data is None:
            raise db.Error("No image data")
        if upload_url is None:
            if handler is None:
                from handlers import ImageUploadHandler
                handler = ImageUploadHandler
            upload_url = handler.get_upload_url()
        image = cls.create_new_entity(source_url=url, **kwargs)
        if filename is None:
            filename = image.key()
        file = UploadFile(data, filename)
        upload_url = blobstore.create_upload_url(upload_url)
        try:
            urllib2.urlopen(upload_url, {'file': file, 'key': str(image.key())})
        except Exception, e:
            pass
        image = cls.get(image.key())
        if image is not None and image.blob_info is None:
            image.delete()
            image = None
        return image
