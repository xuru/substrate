
Restler
=======

Restler at it's most basic level, is a library that can serialize App Engine models and queries to json and xml.
In addition and contains infrastructure and components to help create and manage a JSON/Restful API
using the GAE 'webapp' framework.

Installation
============

Copy the lib/restler directory to your project directory or somewhere that's in 
your app's PYTHONPATH path.


Getting Started
===============

The simple case:

# Restler can create a json string from any data serializable by simplejson.dumps().

>>> from restler.serializers import to_json
>>> to_json({"alist": [1, 2, 3]})
'{"alist": [1, 2, 3]}'

# Serialize all fields in a model from a Query

>>> from restler.serializers import ModelStrategy, SerializationStrategy, to_json, to_xml
>>> from tests.models import Model1, Model2
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


