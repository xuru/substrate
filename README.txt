
Restler
=======

Restler is a set of components to help create and manage a JSON/Restful API
using the GAE 'webapp' framework.

Installation
============

Copy the lib/restler directory to your project directory or somewhere that's in 
your app's PYTHONPATH path.


Getting Started
===============

The simple case:

>>> from restler.serializers import ModelStrategy, SerializationStrategy, to_json, to_xml
>>> from models import Model1, Model2
>>> json = to_json(Model1.all(), ModelStrategy(Model1, include_all_fields=True)) 
>>> xml = to_xml(Model1.all(), ModelStrategy(Model1, include_all_fields=True))

Exclude one field, the 'datetime' property:

>>> json = to_json(Model1.all(), ModelStrategy(Model1, include_all_fields=True) - ["datetime"])

Don't include any fields:

>>> json = to_json(Model1.all(), ModelStrategy(Model1))

Include only one field, the 'datetime':

>>> json = to_json(Model1.all(), ModelStrategy(Model1) + ["datetime"])

Serialize more than one Model (i.e. SerializationStrategy)

>>> ss = ( ModelStrategy(Model1, include_all_fields=True) + 
...        ModelStrategy(Model2, include_all_fields=True) )

>>> type(ss)
<class 'restler.serializers.SerializationStrategy'>

>>> json = to_json(list(Model1.all().fetch(5)) + list(Model1.all().fetch(5)), ss)

See the tests/doctests directory to see more examples of usage and api.py for
a simple example in the context of a webapp.

Integrating with your web framework
===================================

The easiest way to integrate restler with your framework is to use it as a library.

You can, however, use the included 'webapp' adapter to handle the HTTP verbs.  Return
a tuple with the collection (Query/model objects) and a SerializationStrategy or ModelStrategy.


