from __future__ import with_statement

import logging
import mimetypes
import urlparse

from google.appengine.api import images, lib_config, memcache, files, urlfetch

from google.appengine.ext import db, blobstore


class ConfigDefaults(object):
    """Configurable constants.

    To override agar.image configuration values, define values like this
    in your appengine_config.py file (in the root of your app):

        agar_image_DEBUG = True
        agar_image_SERVING_URL_TIMEOUT = 60*60
        agar_image_SERVING_URL_LOOKUP_TRIES = 3
    """
    DEBUG = False
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
            #noinspection PyArgumentList
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
                    #noinspection PyArgumentList
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
    def create(cls, blob_info=None, data=None, filename=None, url=None, mime_type=None, **kwargs):
        if blob_info is not None:
            kwargs['blob_info'] = blob_info
            return cls.create_new_entity(**kwargs)
        if data is None:
            if url is not None:
                response = urlfetch.fetch(url)
                data = response.content
                mime_type = mime_type or response.headers.get('Content-Type', None)
                if filename is None:
                    path = urlparse.urlsplit(url)[2]
                    filename = path[path.rfind('/')+1:]
        if data is None:
            raise db.Error("No image data")
        image = cls.create_new_entity(source_url=url, **kwargs)
        filename = filename or str(image.key())
        mime_type = mime_type or mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        blob_file_name = files.blobstore.create(mime_type=mime_type, _blobinfo_uploaded_filename=filename)
        with files.open(blob_file_name, 'a') as f:
            f.write(data)
        files.finalize(blob_file_name)
        image.blob_info = files.blobstore.get_blob_key(blob_file_name)
        image.put()
        image = cls.get(str(image.key()))
        if image is not None and image.blob_info is None:
            logging.error("Failed to create image: %s" % filename)
            image.delete()
            image = None
        return image
