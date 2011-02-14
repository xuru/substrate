from cStringIO import StringIO
import urllib2
import urllib2_file
import urlparse

from google.appengine.api import images, lib_config, urlfetch

from google.appengine.ext import db, blobstore

from hulk.image.handlers import ImageUploadHandler


class ConfigDefaults(object):
    """Configurable constants.

    To override hulk.image configuration values, define values like this
    in your appengine_config.py file (in the root of your app):

        hulk_image_DEBUG = True
        hulk_image_UPLOAD_HANDLER = The handler to use to POST the image data to.
        hulk_image_UPLOAD_URL = The URL to POST the image data to.
    """
    DEBUG = False
    UPLOAD_HANDLER = ImageUploadHandler
    UPLOAD_URL = '/hulk/image_upload/'

config = lib_config.register('hulk_image', ConfigDefaults.__dict__)

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

    def get_serving_url(self, *args, **kwargs):
        if self.blob_key is not None:
            return images.get_serving_url(str(self.blob_key), *args, **kwargs)
        return None

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
        try:
            result = urllib2.urlopen(upload_url, {'file': file, 'key': str(image.key())})
#            data = urllib2.urlopen(upload_url, {'file': file, 'key': str(image.key())})
#            logging.info("POSTing to %s" % upload_url)
#            response = post_multipart(
#                url,
#                [('key', str(image.key()))],
#                [('file', filename, str(StringIO(data)))]
#            )
#            logging.debug('Post response: %s' % response)
        except Exception, e:
            from hulk.env import on_server
            if on_server:
                import logging
                logging.error("Failed to create image: %s" % e)
                import time
                time.sleep(5)
        image = cls.get(str(image.key()))
        if image is not None and image.blob_info is None:
            image.delete()
            image = None
        return image

import httplib, mimetypes

#def post_multipart(host, selector, fields, files):
def post_multipart(url, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    import logging
    logging.info('Encoding formdata')
    content_type, body = encode_multipart_formdata(fields, files)
    logging.info('POSTing: %s' % body)
    response = urlfetch.fetch(url, body, urlfetch.POST, {'Content-Type': content_type}, False, False)
    logging.info('POSTed')
    return response.status_code


def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
