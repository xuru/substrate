
import datetime
import decimal
import pprint
import types

from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.api import users
from django.utils import simplejson

import datetime_safe

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

class ModelMapping(object):
    """ Defines how to serialize an AppEngine model i.e. which fields to include,
        exclude or map to a callable.  """

    class ModelMappings(object):
        """ A container for multiple mappings (shouldn't be used directly)"""
        def __init__(self, mappings={}):
            if isinstance(mappings, ModelMapping):
                self.mappings = mappings.to_dict()
            else:
                self.mappings = mappings

        def __add__(self, mapping):
            if isinstance(mapping, dict):
                self.mappings.update(mapping)
            elif isinstance(mapping, self.__class__):
                self.mappings.update(mapping.mappings)
            elif isinstance(mapping, ModelMapping):
                self.mappings.update(mapping.to_dict())
            else:
                raise ValueError("Cannot add type: %s" % type(mapping))
            return self

        def __repr__(self):
            return pprint.pformat(self.mappings)

    def __init__(self, model, fields = []):
        self.model = model
        self.fields = fields

    def add(self, field, with_=None):
        if isinstance(field, (tuple, list)):
            self.fields.extend([f for f in field if f not in self.fields])
        elif isinstance(field, dict):
            self.fields.extend([(f, with_) for f, with_ in field if (f, with_) not in self.fields])
        elif with_ is None: 
            if field not in self.fields: 
                self.fields.append(field)
        elif field not in self.fields:
            self.fields.append((field, with_))
        return self

    def to_dict(self): 
        return {self.model: list(self.fields)}

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.ModelMappings(self) + other
        elif isinstance(other, self.ModelMappings):
            return other + self
        else:
            raise ValueError("Cannot add type %s" % type(other))

    def __repr__(self):
        return pprint.pformat(self.to_dict())

def to_json(thing, strategy={}):
    if isinstance(strategy, ModelMapping):
        strategy = strategy.to_dict()
    elif isinstance(strategy, ModelMappings):
        strategy = strategy.mappings
    elif not isinstance(strategy, (dict):
        raise ValueError("Serialization strategy must be a ModelMapping, ModelMappings or dict")
    class AEEncoder(simplejson.JSONEncoder):
        def default(self, obj):
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
                    fields = ( strategy.get(obj.__class__, {}) 
                            or obj.properties().keys() )
                # catch the case where there's just one property (and it's not in a list/tuple)
                if not isinstance(fields, (tuple, list)): 
                    fields = [fields]
                # if any fields use the "-" to exclude a field from 'all' properties
                if any([f.startswith("-") for f in fields if isinstance(f, str)]):
                    obj_fields = obj.properties().keys()
                    for f in fields:
                        if isinstance(f, str) and f.startswith("-") and len(f) > 1: 
                            try:
                                obj_fields.remove(f[1:])
                            except ValueError:
                                raise ValueError( "'%s' can't be excluded. " 
                                        + "It isn't a valid property of %s" 
                                        % (f[1:], obj.__class__.__name__))
                        elif f not in obj_fields:
                            obj_fields.append(f)
                    fields = obj_fields
                callable_ = None
                for field_name in fields:
                    if isinstance(field_name, (tuple, list)):
                        field_name, callable_ = field_name
                        if isinstance(callable_, str):
                            callable_ = ( globals().get(callable_, None) 
                                        or getattr(obj.__class__, callable_, None) )
                        if not callable_:
                            raise ValueError("'%s' was not found or is not callable" % callable_name)
                    elif isinstance(field_name, str):
                        attr = ( globals().get(field_name, None)
                                    or getattr(obj.__class__, field_name, None) )
                        if callable(attr): callable_ = attr
                    if callable_:
                        ret[field_name] = callable_(obj)
                    else:
                        ret[field_name] = getattr(obj, field_name) 
            return ret
    return simplejson.dumps(thing, cls=AEEncoder)


