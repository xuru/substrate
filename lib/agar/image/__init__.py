from cStringIO import StringIO
import logging
import time
import urllib2
import urllib2_file
import urlparse

from google.appengine.api import images, lib_config, memcache

from google.appengine.ext import db, blobstore

from agar.env import on_server
from agar.image.handlers import ImageUploadHandler


class ConfigDefaults(object):
    """Configurable constants.

    To override agar.image configuration values, define values like this
    in your appengine_config.py file (in the root of your app):

        agar_image_DEBUG = True
        agar_image_UPLOAD_HANDLER = The handler to use to POST the image data to.
        agar_image_UPLOAD_URL = The URL to POST the image data to.
    """
    DEBUG = False
    UPLOAD_HANDLER = ImageUploadHandler
    UPLOAD_URL = '/agar/image_upload/'
    MAX_UPLOAD_TRIES = 3
    SERVING_URL_TIMEOUT = 60*60
    SERVING_URL_LOOKUP_TRIES = 3

config = lib_config.register('agar_image', ConfigDefaults.__dict__)

class Image(db.Model):
    blob_info = blobstore.BlobReferenceProperty(required=False, default=None)
    source_url = db.StringProperty(required=False, default=None)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

    #noinspection PyUnresolvedReferences
    @property
    def blob_key(self):
        if self.blob_info is not None:
            return self.blob_info.key()
        return None

    @property
    def image(self):
        if self.blob_key is not None:
            return images.Image(blob_key=self.blob_key)
        return None

    @property
    def width(self):
        if self.image is not None:
            return self.image.width
        return None
    
    @property
    def height(self):
        if self.image is not None:
            return self.image.height
        return None

    @property
    def image_data(self):
        if self.blob_key is not None:
            return blobstore.BlobReader(self.blob_key).read()
        return None

    def get_serving_url(self, size=None, crop=False):
        serving_url = None
        if self.blob_key is not None:
            namespace = "agar-image-serving-url"
            key = "%s-%s-%s" % (self.key().name(), size, crop)
            serving_url = memcache.get(key, namespace=namespace)
            if serving_url is None:
                tries = 0
                while tries < config.SERVING_URL_LOOKUP_TRIES:
                    try:
                        tries += 1
                        serving_url = images.get_serving_url(str(self.blob_key), size=size, crop=crop)
                        if serving_url is not None:
                            break
                    except Exception, e:
                        if tries >= config.SERVING_URL_LOOKUP_TRIES:
                            logging.error("Unable to get image serving URL: %s" % e)
                if serving_url is not None:
                    memcache.set(key, serving_url, time=config.SERVING_URL_TIMEOUT, namespace=namespace)
        return serving_url

    #noinspection PyUnresolvedReferences
    def delete(self, **kwargs):
        if self.blob_info is not None:
            self.blob_info.delete()
        super(Image, self).delete(**kwargs)

    @classmethod
    def create_new_entity(cls, **kwargs):
        image = cls(**kwargs)
        image.put()
        return image

    @classmethod
    def create(cls, blob_info=None, data=None, filename=None, url=None, upload_url=None, **kwargs):
        if blob_info is not None:
            kwargs['blob_info'] = blob_info
            return cls.create_new_entity(**kwargs)
        if data is None:
            if url is not None:
                data = StringIO(urllib2.urlopen(url).read())
                if filename is None:
                    path = urlparse.urlsplit(url)[2]
                    filename = path[path.rfind('/')+1:]
        else:
            data = StringIO(str(data))
        if data is None:
            raise db.Error("No image data")
        if upload_url is None:
            upload_url = config.UPLOAD_URL
        image = cls.create_new_entity(source_url=url, **kwargs)
        if filename is None:
            filename = str(image.key())
        file = urllib2_file.UploadFile(data, filename)
        upload_url = blobstore.create_upload_url(upload_url)
        tries = 0
        e = None
        while tries < config.MAX_UPLOAD_TRIES:
            try:
                image = cls.get(str(image.key()))
                if image is not None and image.blob_info is not None:
                    break
                result = urllib2.urlopen(upload_url, {'file': file, 'key': str(image.key())})
                logging.debug('Post response: %s' % result)
                break
            except Exception, e:
                if on_server:
                    tries += 1
                    time.sleep(1)
                else:
                    break
        image = cls.get(str(image.key()))
        if image is not None and image.blob_info is None:
            if on_server:
                logging.error("Failed to create image: %s" % e)
            image.delete()
            image = None
        return image
