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

.. autofunction:: agar.auth.authenticate_https
.. autofunction:: agar.auth.authentication_required
.. autofunction:: agar.auth.https_authentication_required

.. autoclass:: agar.config.Config
    :members:

.. autofunction:: agar.dates.parse_datetime

.. autofunction:: agar.django.decorators.validate_service

.. autodata:: agar.env.on_development_server
.. autodata:: agar.env.on_integration_server
.. autodata:: agar.env.on_production_server
.. autodata:: agar.env.on_server

.. autoclass:: agar.json.JsonRequestHandler
    :members:
    :undoc-members:

.. autoclass:: agar.json.MultiPageHandler
    :members:
    :undoc-members:

.. autoclass:: agar.json.CorsMultiPageHandler
    :members:

.. autoclass:: agar.models.NamedModel
    :members:

.. autodata:: agar.templatetags.webapp2.url_for
.. autodata:: agar.templatetags.webapp2.on_production_server

.. autofunction:: agar.url.url_for

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

