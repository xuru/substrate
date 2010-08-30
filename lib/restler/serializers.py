
import datetime
import decimal
import pprint
import types

from xml.sax import saxutils
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

class ModelStrategy(object):
    """ Defines how to serialize an AppEngine model i.e. which fields to include,
        exclude or map to a callable.  """

    class SerializationStrategy(object):
        """ A container for multiple mappings (shouldn't be used directly)"""
        def __init__(self, mappings={}):
            if isinstance(mappings, ModelStrategy):
                self.mappings = mappings.to_dict()
            else:
                self.mappings = dict(mappings.items())

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

    def __init__(self, model, include_all_fields=False):
        self.model = model
        if include_all_fields:
            self.fields = [f for f in model.fields()]
        else:
            self.fields = fields = []

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
        m = ModelStrategy(self.model)
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
                    if name in self.model.fields():
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
        m = ModelStrategy(self.model) + self.fields
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
        return {self.model: list(self.fields)}

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.SerializationStrategy(self) + other
        elif isinstance(other, self.SerializationStrategy):
            return other + self
        elif isinstance(other, (list, tuple, basestring)):
            return self.__add(other)
        else:
            raise ValueError("Cannot add type %s" % type(other))

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            raise ValueError("Cannot subtract type %s" % type(other))
        elif isinstance(other, self.SerializationStrategy):
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

def encoder_builder(type_, strategy={}):
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
            # User the model's properties
            if strategy is None:
                fields = obj.properties().keys()
            else:
                # Load the customized mappings
                fields = strategy.get(obj.__class__, None)
                if fields is None:
                    fields = obj.properties().keys()
            # catch the case where there's just one property (and it's not in a list/tuple)
            if not isinstance(fields, (tuple, list)):
                fields = [fields]
            target = None
            for field_name in fields:
                # Check to see if this remaps a field to a callable or a different field
                if isinstance(field_name, dict):
                    field_name, target = field_name.items()[0] # Only one key/value
                if callable(target): # Defer to the callable
                    ret[field_name] = target(obj)
                else:
                    if target: # Remapped name
                        if hasattr(obj, target):
                            ret[field_name] = getattr(obj, target)
                        else:
                            raise ValueError("'%s' was not found " % target)
                    else: # Common case (just the field)
                        ret[field_name] = getattr(obj, field_name) 
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


def to_json(thing, strategy={}):
    if isinstance(strategy, ModelStrategy):
        strategy = strategy.to_dict()
    elif isinstance(strategy, ModelStrategy.SerializationStrategy):
        strategy = strategy.mappings
    elif not isinstance(strategy, dict):
        raise ValueError("Serialization strategy must be a ModelStrategy, SerializationStrategy or dict")
    encoder = encoder_builder("json", strategy)
    return simplejson.dumps(thing, cls=encoder)


def _encode_xml(thing, node, strategy, xml_style):
    encoder = encoder_builder("xml", strategy)
    # Easy types to convert to unicode
    simple_types = (bool, basestring, int, long, float, decimal.Decimal)
    collection_types = (list, dict)
    if isinstance(thing, db.Model):
        el = xml_style["model"](node, thing)
        if el is None: el = node
        _encode_xml(encoder(thing), el, strategy, xml_style)
        return
    elif isinstance(thing, dict):
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
                    _encode_xml(value, e, strategy, xml_style)
                else:
                    _encode_xml(encoder(value), e, strategy, xml_style)
            else:
                e.text = unicode(value)
        return 
    elif isinstance(thing, list):
        # Allow overriding default
        el = xml_style["list"](node, thing)
        if el is None: el = node
        for value in thing:
            i = xml_style["list_item"](el, value)
            if not isinstance(value, simple_types):
                if isinstance(value, collection_types):
                    _encode_xml(value, i, strategy, xml_style)
                else:
                    _encode_xml(encoder(value), i, strategy, xml_style)
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
        _encode_xml(encoder(thing), node, strategy, xml_style)
    return


DEFAULT_XML_STYLE = {
            "root": lambda thing: ET.Element("result"),
            "model": lambda el, thing: ET.SubElement(el, thing.kind().lower()),
            "list": lambda el, thing: None, # top level element for a list
            "list_item": lambda el, thing: ET.SubElement(el, "item"), # An item in a list
            "dict": lambda el, thing: None, # top level element for a dict
            "dict_item": lambda el, thing: ET.SubElement(el, thing[0]), # thing is tuple(key, value)
            "null": lambda el, thing: el.set("null", "true"),
} 

def to_xml(thing, strategy={}, xml_style=DEFAULT_XML_STYLE):
    if isinstance(strategy, ModelStrategy):
        strategy = strategy.to_dict()
    elif isinstance(strategy, ModelStrategy.SerializationStrategy):
        strategy = strategy.mappings
    elif not isinstance(strategy, dict):
        raise ValueError("Serialization strategy must be a ModelStrategy, SerializationStrategy or dict")

    root = xml_style["root"](thing)
    _encode_xml(thing, root, strategy, xml_style)
    return ET.tostring(root)


