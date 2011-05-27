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
.. autoclass:: agar.models.NamedModel
    :members:

-----------------
agar.templatetags
-----------------
.. autodata:: agar.templatetags.webapp2.url_for
.. autodata:: agar.templatetags.webapp2.on_production_server

--------
agar.url
--------
.. autofunction:: agar.url.url_for

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

