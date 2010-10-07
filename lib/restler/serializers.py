
import copy
import datetime
import decimal
import pprint
import types

from xml.etree import ElementTree as ET

from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.api import datastore
from google.appengine.api import datastore_types
from google.appengine.api import users
from django.utils import simplejson


import datetime_safe

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

DEFAULT_STYLE = {
    'xml' : {
        "root": lambda thing: ET.Element("result"),
        "model": lambda el, thing: ET.SubElement(el, thing.kind().lower()),
        "list": lambda el, thing: None, # top level element for a list
        "list_item": lambda el, thing: ET.SubElement(el, "item"), # An item in a list
        "dict": lambda el, thing: None, # top level element for a dict
        "dict_item": lambda el, thing: ET.SubElement(el, thing[0]), # thing is tuple(key, value)
        "null": lambda el, thing: el.set("null", "true"),
    },
    'json' : {
        "flatten" : True,
    }
} 

class SerializationStrategy(object):
    """ A container for multiple mappings (shouldn't be used directly)"""
    def __init__(self, mappings={}, style=None):
        if isinstance(mappings, ModelStrategy):
            self.mappings = mappings.to_dict()
        else:
            self.mappings = dict(mappings.items())
        if style == None:
            self.style = copy.deepcopy(DEFAULT_STYLE)
        else:
            self.style = style

    def _new_mapping(self, other_dict):
        maps = dict(self.mappings.items())
        maps.update(other_dict)
        return self.__class__(maps)

    def __add__(self, mapping):
        if isinstance(mapping, dict):
            return self._new_mapping(mapping)
        elif isinstance(mapping, self.__class__):
            return self._new_mapping(mapping.mappings)
        elif isinstance(mapping, ModelStrategy):
            return self._new_mapping(mapping.to_dict())
        else:
            raise ValueError("Cannot add type: %s" % type(mapping))
        return self

    def __sub__(self, mapping):
        if isinstance(mapping, ModelStrategy):
            m = self._new_mapping(mapping.to_dict())
        else:
            raise ValueError("Not of type ModelStrategy")

    def __repr__(self):
        return pprint.pformat(self.mappings)

class ModelStrategy(object):
    """ Defines how to serialize an AppEngine model i.e. which fields to include,
        exclude or map to a callable.
    """

    def __init__(self, model, include_all_fields=False, output_name=None):
        """
        model - The App Engine model class to be serialized.
        
        keyname arguments:
        include_all_fields=False Creates a strategy with all properties of the Model to be serialized.
        output_name=None [None|string|callable] The key or tag that surrounds the serialized properties for a Model. 
            The default value is the lowercase classname of the Model.
            None flattens the result structure. 
                with name:  [{'my_class':{'prop1':'value1'}}, ...]
                without name:  [{'prop1':'value1'}, ...]
        """
        self.model = model
        if include_all_fields:
            self.fields = [f for f in model.fields()]
        else:
            self.fields = fields = []
        self.name = output_name

    def __name_map(self):
        # We remove 'properties' i.e. things with callables by name
        # so we create a list of names that can be deleted
        names = {};
        for p in self.fields:
            if isinstance(p, dict):
                names[p.keys()[0]] = p
            elif isinstance(p, basestring):
                names[p] = p
        return names

    def __add(self, fields):
        names = self.__name_map()
        m = ModelStrategy(self.model, output_name=self.name)
        m.fields = self.fields[:]
        if isinstance(fields, (tuple, list)):
            for name in fields:
                if isinstance(name, dict):
                    if len(name.keys()) != 1:
                        raise ValueError("Mapping is not a 1-1 name -> field/callable")
                    else:
                        prop = name
                        name = name.keys()[0]
                        if name not in names:
                            m.fields.append(prop)
                            names[name] = prop
                        else:
                            raise ValueError("Cannot add field.  '%s' already exists" % name)
                elif name not in names:
                    if (name in self.model.fields()
                            or isinstance(getattr(self.model, name, None), property)
                            or callable(getattr(self.model, name, None))):
                        m.fields.append(name)
                        names[name] = name
                    else:
                        raise ValueError("Cannot add field.  '%s' is not a valid field for model '%s'" % (name, self.model ))
                else:
                    raise ValueError("Cannot add field.  '%s' already exists" % (name, ))
        else:
            raise ValueError("Only lists/tuples or fields can be added")
        return m

    def __remove(self, fields):
        m = ModelStrategy(self.model, output_name=self.name) + self.fields
        names = self.__name_map()
        if isinstance(fields, (tuple, list)):
            for f in fields:
                # if they're giving us the field -> callable mapping, we just want the field
                if isinstance(f, dict):
                    f, _ = f.items()[0]
                if f in names:
                    m.fields.remove(names[f])
                else:
                    raise ValueError("'%s' cannot be removed. It is not in the current fields list (%s)" % (f, self.fields))
        else:
            raise ValueError("Fields must be a tuple or list.")
        return m

    def to_dict(self): 
        if self.name is not None:
            return {self.model: {self.name: self.fields}}
        return {self.model: self.fields}

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return SerializationStrategy(self) + other
        elif isinstance(other, SerializationStrategy):
            return other + self
        elif isinstance(other, (list, tuple, basestring)):
            return self.__add(other)
        else:
            raise ValueError("Cannot add type %s" % type(other))

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            raise ValueError("Cannot subtract type %s" % type(other))
        elif isinstance(other, SerializationStrategy):
            return other - self
        elif isinstance(other, (list, tuple, basestring)):
            return self.__remove(other)
        else:
            raise ValueError("Cannot add type %s" % type(other))

    def __lshift__(self, other):
        """ Shorthand for overriding fields with new behavior
            i.e. remove the fields and add back in with new mappings"""
        if not isinstance(other, (list, tuple, basestring)):
            raise ValueError("Cannot add type %s" % type(other))
        return self.__remove(other).__add(other)

    def __repr__(self):
        return pprint.pformat(self.to_dict())

def encoder_builder(type_, strategy=None, style=None):
    def default_impl(obj):
        # Load objects from the datastore (could be done in parallel)
        if isinstance(obj, db.Query):
            return [o for o in obj]
        if isinstance(obj, datetime.datetime):
            d = datetime_safe.new_datetime(obj)
            return d.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))
        elif isinstance(obj, datetime.date):
            d = datetime_safe.new_date(obj)
            return d.strftime(DATE_FORMAT)
        elif isinstance(obj, datetime.time):
            return obj.strftime(TIME_FORMAT)
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))
        elif isinstance(obj, datetime.date):
            return obj.strftime(DATE_FORMAT)
        elif isinstance(obj, datetime.time):
            return obj.strftime(TIME_FORMAT)
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, db.GeoPt):
            return "%s %s" % (obj.lat, obj.lon)
        if isinstance(obj, db.IM):
            return "%s %s" % (obj.protocol, obj.address)
        if isinstance(obj, users.User):
            return user_id() or obj.email()
        if isinstance(obj, blobstore.BlobInfo):
            return str(obj.key()) # TODO is this correct?
        ret = {} # What we're most likely going to return (populated, of course)
        if isinstance(obj, db.Model):
            model = {}
            kind = obj.kind().lower()
            # User the model's properties
            if strategy is None:
                fields = obj.properties().keys()
            else:
                # Load the customized mappings
                fields = strategy.get(obj.__class__, None)
                if fields is None:
                    fields = obj.properties().keys()
                # If it's a dict, we're changing the output_name for the model
                elif isinstance(fields, dict):
                    if len(fields.keys()) != 1:
                        raise ValueError('fields must an instance dict(<model name>=<field list>)')
                    kind, fields = fields.items()[0]
                    # if kind is callable, we'll call it to get the output_name
                    if callable(kind):
                        kind = kind(obj)
            # Handle the case where we don't want the model name as part of the serialization
            if type_ == 'json' and bool(style['json']["flatten"]):
                model = ret
            else:
                ret[unicode(kind)] = model
            # catch the case where there's just one property (and it's not in a list/tuple)
            if not isinstance(fields, (tuple, list)):
                fields = [fields]
            target = None
            for field_name in fields:
                # Check to see if this remaps a field to a callable or a different field
                if isinstance(field_name, dict):
                    field_name, target = field_name.items()[0] # Only one key/value

                if callable(target): # Defer to the callable
                    model[field_name] = target(obj)
                else:
                    if target: # Remapped name
                        if hasattr(obj, target):
                            model[field_name] = getattr(obj, target)
                        else:
                            raise ValueError("'%s' was not found " % target)
                    else: # Common case (just the field)
                        model[field_name] = getattr(obj, field_name) 
        return ret
    if type_ == "json":
        class AEEncoder(simplejson.JSONEncoder):
            def default(self, obj):
                return default_impl(obj)
        return AEEncoder
    elif type_ == "xml":
        return default_impl
    else:
        raise ValueError("type is required to be 'xml' or 'json'")
    return None


def to_json(thing, strategy=None):
    if not isinstance(strategy, (ModelStrategy, SerializationStrategy, types.NoneType)):
        raise ValueError("Serialization strategy must be a ModelStrategy, SerializationStrategy or dict")
    if isinstance(strategy, ModelStrategy):
        strategy = SerializationStrategy(strategy)
    if strategy is None:
        strategy = SerializationStrategy()
    mappings = strategy.mappings
    style = strategy.style
    encoder = encoder_builder("json", mappings, style)
    return simplejson.dumps(thing, cls=encoder)


def _encode_xml(thing, node, strategy, style):
    xml_style = style["xml"]
    encoder = encoder_builder("xml", strategy, style)
    # Easy types to convert to unicode
    simple_types = (bool, basestring, int, long, float, decimal.Decimal)
    collection_types = (list, dict)
    if isinstance(thing, dict):
        # Might seem a little weird how we serialize dictionaries, but in this case
        # the inspiration is from json (where objects define a consistent structure)
        # so we use a <key>value</key> format
        # Allow overriding default
        el = xml_style["dict"](node, thing)
        if el is None: el = node
        for key, value in thing.items():
            if not isinstance(key, basestring):
                raise ValueError("key is not a valid string") # TODO better error message needed
            e = xml_style["dict"](el, (key, value))
            e = ET.SubElement(el, key)
            if value is None:
                xml_style["null"](e, None) 
            elif not isinstance(value, simple_types):
                if isinstance(value, collection_types):
                    _encode_xml(value, e, strategy, style)
                else:
                    _encode_xml(encoder(value), e, strategy, style)
            else:
                e.text = unicode(value)
        return 
    elif isinstance(thing, list):
        # Allow overriding default
        el = xml_style["list"](node, thing)
        if el is None: el = node
        for value in thing:
            if isinstance(value, db.Model):
                # Note: we don't create an item in this circumstance
                _encode_xml(encoder(value), el, strategy, style)
                continue
            i = xml_style["list_item"](el, value)
            if not isinstance(value, simple_types):
                if isinstance(value, collection_types):
                    _encode_xml(value, i, strategy, style)
                else:
                    _encode_xml(encoder(value), i, strategy, style)
            else:
                i.text = unicode(value)
            if value is None:
                xml_style["null"](i, None) 
        return
    elif isinstance(thing, simple_types):
        node.text = unicode(thing)
    elif thing is None:
        xml_style["null"](node, None) 
    else:
        _encode_xml(encoder(thing), node, strategy, style)
    return


def to_xml(thing, strategy=None):
    if not isinstance(strategy, (ModelStrategy, SerializationStrategy)):
        raise ValueError("Serialization strategy must be a ModelStrategy, SerializationStrategy or dict")
    if isinstance(strategy, ModelStrategy):
        strategy = SerializationStrategy(strategy)

    style = strategy.style
    mappings = strategy.mappings

    root = style["xml"]["root"](thing)
    _encode_xml(thing, root, mappings, style)
    return ET.tostring(root)


