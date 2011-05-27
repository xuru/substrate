"""
The ``agar.image`` module contains classes to help work with images stored in the
`Blobstore <http://code.google.com/appengine/docs/python/blobstore/>`_.
"""

from __future__ import with_statement

import logging
import mimetypes
import urlparse

from google.appengine.api import images, memcache, files, urlfetch

from google.appengine.ext import db, blobstore

from agar.config import Config


class ImageConfig(Config):
    """
    :py:class:`~agar.config.Config` settings for the ``agar.image`` library.
    Settings are under the ``agar_image`` namespace.

    The following settings (and defaults) are provided::
    
        agar_image_SERVING_URL_TIMEOUT = 60*60
        agar_image_SERVING_URL_LOOKUP_TRIES = 3
        agar_image_VALID_MIME_TYPES = ['image/jpeg', 'image/png', 'image/gif']

    To override ``agar.image`` settings, define values in the ``appengine_config.py`` file in the root of your app.
    """
    _namepace = 'agar_image'

    #: How long (in seconds) to cache the image serving URL (Default: ``60*60`` or one hour).
    SERVING_URL_TIMEOUT = 60*60
    #: How many times to try to download an image from a URL (Default: ``3``).
    SERVING_URL_LOOKUP_TRIES = 3
    #: Valid image mime types (Default: ``['image/jpeg', 'image/png', 'image/gif']``).
    VALID_MIME_TYPES = ['image/jpeg', 'image/png', 'image/gif']

#: The configuration object for ``agar.image`` settings.
config = ImageConfig.get_config()


class Image(db.Model):
    """
    A model class that helps create and work with images stored in the `Blobstore <http://code.google.com/appengine/docs/python/blobstore/>`_.
    Please note that you should never call the constructor for this class directly when creating an image.  Instead, use
    the :py:meth:`create` method.
    """
    #: The `BlobInfo <http://code.google.com/appengine/docs/python/blobstore/blobinfoclass.html>`_ entity for the image's Blobstore value.
    blob_info = blobstore.BlobReferenceProperty(required=False, default=None)
    #: The original URL that the image data was fetched from, if applicable.
    source_url = db.StringProperty(required=False, default=None)
    #: The create timestamp.
    created = db.DateTimeProperty(auto_now_add=True)
    #: The last modified timestamp.
    modified = db.DateTimeProperty(auto_now=True)

    #noinspection PyUnresolvedReferences
    @property
    def blob_key(self):
        """
        The `BlobKey <http://code.google.com/appengine/docs/python/blobstore/blobkeyclass.html>`_ entity for the image's Blobstore value.
        """
        if self.blob_info is not None:
            return self.blob_info.key()
        return None

    @property
    def image(self):
        """
        The Google `Image <http://code.google.com/appengine/docs/python/images/imageclass.html>`_ entity for the image.
        """
        if self.blob_key is not None:
            return images.Image(blob_key=self.blob_key)
        return None

    @property
    def format(self):
        """
        The format of the image (see `Image.format <http://code.google.com/appengine/docs/python/images/imageclass.html#Image_format>`_
        documentation for possible values). If there is no image data, this will be ``None``.
        """
        if self.image is not None:
            return self.image.format
        return None

    @property
    def width(self):
        """
        The width of the image in pixels (see `Image.width <http://code.google.com/appengine/docs/python/images/imageclass.html#Image_width>`_
        for more documentation). If there is no image data, this will be ``None``.
        """
        if self.image is not None:
            return self.image.width
        return None
    
    @property
    def height(self):
        """
        The height of the image in pixels (see `Image.height <http://code.google.com/appengine/docs/python/images/imageclass.html#Image_height>`_
        for more documentation). If there is no image data, this will be ``None``.
        """
        if self.image is not None:
            return self.image.height
        return None

    @property
    def image_data(self):
        """
        The raw image data as returned by a `BlobReader <http://code.google.com/appengine/docs/python/blobstore/blobreaderclass.html>`_.
        If there is no image data, this will be ``None``.
        """
        if self.blob_key is not None:
            return blobstore.BlobReader(self.blob_key).read()
        return None

    def get_serving_url(self, size=None, crop=False):
        """
        Returns the serving URL for the image. Works just like the Google Images API function
        `get_serving_url <http://code.google.com/appengine/docs/python/images/functions.html#Image_get_serving_url>`_,
        but adds caching. The cache timeout is controlled by the :py:attr:`.SERVING_URL_TIMEOUT` setting.

        Keyword arguments
        (see Google's Image API function, `get_serving_url <http://code.google.com/appengine/docs/python/images/functions.html#Image_get_serving_url>`_
        for more detailed argument information):
        
            ``size`` -- An integer supplying the size of resulting images.

            ``crop`` -- Specify ``true`` for a cropped image, and ``false`` for a resized image.
        """
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
        """
        Delete the image and its attached Blobstore storage.
        """
        if self.blob_info is not None:
            self.blob_info.delete()
        super(Image, self).delete(**kwargs)

    @classmethod
    def create_new_entity(cls, **kwargs):
        """
        Called to create a new entity. The default implementation simply creates the entity with the default constructor
        and calls ``put()``. This method allows the class to be mixed-in with :py:class:`agar.models.NamedModel`.
        """
        image = cls(**kwargs)
        image.put()
        return image

    @classmethod
    def create(cls, blob_info=None, data=None, filename=None, url=None, mime_type=None, **kwargs):
        """
        Create an Image. Use this class method rather than creating an image with the constructor. You must provide one
        of the following parameters ``blob_info``, ``data``, or ``url`` to specify the image data to use.

        Keyword arguments
            ``blob_info`` -- The blobstore data to use as the image data. If this parameter is not ``None``, all other
            parameters will be ignored as they aren't needed.

            ``data`` -- The image data that should be put in the blobstore and used as the image data.

            ``filename`` -- The filename of the image data. If not provided, the filename will be guessed from the URL
            or, if there is no URL, it will be set to the stringified `Key <http://code.google.com/appengine/docs/python/datastore/keyclass.html>`_
            of the image entity.

            ``url`` - The URL to fetch the image data from and then place in the blobstore to be used as the image data.

            ``mime_type`` -- The `mime type <http://en.wikipedia.org/wiki/Internet_media_type>`_ to use for the blobstore
            image data. If ``None``, it will attempt to guess the mime type from the url fetch response headers or the
            filename.

        Keyword arguments inherited from `Model <http://code.google.com/appengine/docs/python/datastore/modelclass.html>`_
            ``parent`` -- The `Model <http://code.google.com/appengine/docs/python/datastore/modelclass.html>`_ instance
            or `Key <http://code.google.com/appengine/docs/python/datastore/keyclass.html>`_ instance for the entity
            that is the new image's parent.

            ``key_name`` -- The name for the new entity. The name becomes part of the primary key.

            ``**kwargs`` -- Initial values for the instance's properties, as keyword arguments.  Useful if subclassing.

            ``key`` -- The explicit `Key <http://code.google.com/appengine/docs/python/datastore/keyclass.html>`_ instance
            for the new entity. Cannot be used with key_name or parent. If None, falls back on the behavior for key_name
            and parent.
        """
        if filename is not None:
            filename = filename.encode('ascii', 'ignore')
        if url is not None:
            url = url.encode('ascii', 'ignore')
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
        if mime_type not in config.VALID_MIME_TYPES:
            message = "The image mime type (%s) isn't valid" % mime_type
            logging.warning(message)
            image.delete()
            raise images.BadImageError(message)
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
