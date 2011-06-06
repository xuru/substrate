.. Substrate documentation master file, created by
   sphinx-quickstart on Fri May 20 23:04:53 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Substrate's documentation!
=====================================

Contents:

.. toctree::
   :maxdepth: 2

   downloads

====
agar
====
.. automodule:: agar

---------
agar.auth
---------
.. automodule:: agar.auth
    :members: authentication_required, https_authentication_required, https_authenticate, AuthConfig

-----------
agar.config
-----------
.. automodule:: agar.config
.. autoclass:: agar.config.Config
    :members: _namespace, get_config

----------
agar.dates
----------
.. automodule:: agar.dates
    :members:

-----------
agar.django
-----------
.. automodule:: agar.django

^^^^^^^^^^^^^^^^^^^^^^
agar.django.decorators
^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: agar.django.decorators
    :members:

--------
agar.env
--------
.. automodule:: agar.env
    :members:

----------
agar.image
----------
.. automodule:: agar.image
.. autoclass:: agar.image.Image()
    :members:
    :exclude-members: create

    .. automethod:: create(blob_info=None, data=None, filename=None, url=None, mime_type=None, parent=None, key_name=None)

.. autoclass:: agar.image.ImageConfig
    :members:

---------
agar.json
---------
.. autoclass:: agar.json.JsonRequestHandler
    :members:
    :undoc-members:

.. autoclass:: agar.json.MultiPageHandler
    :members:
    :undoc-members:

.. autoclass:: agar.json.CorsMultiPageHandler
    :members:

-----------
agar.models
-----------
.. automodule:: agar.models

.. autoclass:: agar.models.NamedModel
    :members:
    :exclude-members: create_new_entity

    .. automethod:: create_new_entity(key_name=None, parent=None, **kwargs)

.. autoclass:: DuplicateKeyError
.. autoclass:: ModelException


-----------------
agar.templatetags
-----------------
.. autodata:: agar.templatetags.webapp2.url_for
.. autodata:: agar.templatetags.webapp2.on_production_server

--------
agar.url
--------
.. automodule:: agar.url

=================
restler
=================
.. autoclass:: restler.serializers.ModelStrategy
    :members:
.. autoclass:: restler.serializers.SerializationStrategy
    :members:
.. autofunction:: restler.serializers.json_response
.. autofunction:: restler.serializers.xml_response


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. Links

.. _Google App Engine python: http://code.google.com/appengine/docs/python/overview.html
.. _Key: http://code.google.com/appengine/docs/python/datastore/keyclass.html
.. _key().name(): http://code.google.com/appengine/docs/python/datastore/keyclass.html#Key_name
.. _Model: http://code.google.com/appengine/docs/python/datastore/modelclass.html
.. _Blobstore: http://code.google.com/appengine/docs/python/blobstore/
.. _BlobInfo: http://code.google.com/appengine/docs/python/blobstore/blobinfoclass.html
.. _BlobKey: http://code.google.com/appengine/docs/python/blobstore/blobkeyclass.html
.. _BlobReader: http://code.google.com/appengine/docs/python/blobstore/blobreaderclass.html
.. _Image: http://code.google.com/appengine/docs/python/images/imageclass.html
.. _Image.format: http://code.google.com/appengine/docs/python/images/imageclass.html#Image_format
.. _Image.width: http://code.google.com/appengine/docs/python/images/imageclass.html#Image_width
.. _Image.height: http://code.google.com/appengine/docs/python/images/imageclass.html#Image_height
.. _Image.get_serving_url: http://code.google.com/appengine/docs/python/images/functions.html#Image_get_serving_url
.. _google.appengine.api.lib_config: http://code.google.com/p/googleappengine/source/browse/trunk/python/google/appengine/api/lib_config.py

.. _django: http://www.djangoproject.com/
.. _django forms: https://docs.djangoproject.com/en/dev/topics/forms/
.. _django form class: https://docs.djangoproject.com/en/1.3/ref/forms/api/#django.forms.Form

.. _webapp2: http://code.google.com/p/webapp-improved/
.. _webapp2.Request: http://webapp-improved.appspot.com/api.html#webapp2.Request
.. _webapp2.RequestHandler: http://webapp-improved.appspot.com/api.html#webapp2.RequestHandler
.. _webapp2.RequestHandler.abort: http://webapp-improved.appspot.com/api.html#webapp2.RequestHandler.abort

.. _uuid4: http://docs.python.org/library/uuid.html#uuid.uuid4

.. _mime type: http://en.wikipedia.org/wiki/Internet_media_type