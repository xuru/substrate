
import datetime
import decimal
import types

from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.api import users
from django.utils import simplejson

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

"""
    def default(self, o):
        if isinstance(o, datetime.datetime):
            d = datetime_safe.new_datetime(o)
            return d.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT))
        elif isinstance(o, datetime.date):
            d = datetime_safe.new_date(o)
            return d.strftime(self.DATE_FORMAT)
        elif isinstance(o, datetime.time):
            return o.strftime(self.TIME_FORMAT)
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            return super(DjangoJSONEncoder, self).default(o)
"""

def to_json(thing, strategy={}):
    if not isinstance(strategy, dict):
        raise ValueError("Serialization strategy must be a dictionary")
    class AEEncoder(simplejson.JSONEncoder):
        def default(self, obj):
            # Load objects from the datastore (could be done in parallel)
            if isinstance(obj, db.Query):
                return [o for o in obj]
            """
            if isinstance(obj, datetime.datetime):
                d = datetime_safe.new_datetime(obj)
                return d.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT))
            elif isinstance(obj, datetime.date):
                d = datetime_safe.new_date(obj)
                return d.strftime(self.DATE_FORMAT)
            elif isinstance(obj, datetime.time):
                return obj.strftime(self.TIME_FORMAT)
            """
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


