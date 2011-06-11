"""The ``restler`` package is a simple and flexible serialization to JSON and XML of App Engine Models and Queries.


Simple example:

>>> from google.appengine.ext import db
>>> from restler.serializers import ModelStrategy, SerializationStrategy, to_json, to_xml, SKIP
>>>

First, let's create a simple db Model class that we'll later serialize.

>>> class Person(db.Model):
...     first_name = db.StringProperty()
...     last_name = db.StringProperty()
...     ssn = db.StringProperty()
>>>

Next, we'll create an instance of the Person class.

>>> jean = Person(first_name="Jeanne", last_name="d'Arc", ssn="N/A")
>>>

Now, let's try serializing it:

>>> to_json(jean)
'{"first_name": "Jeanne", "last_name": "d\'Arc", "ssn": "N/A"}'

Perfect, that's exactly what we wanted.  
>>> to_json(jean, ModelStrategy(Person, include_all_fields=True))
'{"first_name": "Jeanne", "last_name": "d\'Arc", "ssn": "N/A"}'

"""