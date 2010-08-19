
import types

from google.appengine.ext import db
from django.utils import simplejson


def to_json(thing, serialization_mapper={}):
    class AEEncoder(simplejson.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, db.Query):
                return [o for o in obj]
            ret = {}
            if isinstance(obj, db.Model):
                if serialization_mapper is None:
                    fields = obj.properties().keys() 
                else:
                    fields = ( serialization_mapper.get(obj.__class__, []) 
                            or obj.properties().keys() )
                # if any fields use the "-" to exclude a field from 'all' properties
                if not isinstance(fields, (tuple, list)): 
                    fields = [fields]
                if any([f.startswith("-") for f in fields if isinstance(f, str)]):
                    fields_ = obj.properties().keys()
                    for f in fields:
                        if f.startswith("-") and len(f) > 1: 
                            try:
                                fields_.remove(f[1:])
                            except ValueError:
                                raise ValueError( "'%s' can't be excluded. " 
                                        + "It isn't a valid property of %s" 
                                        % (f[1:], obj.__class__.__name__))
                        elif f not in fields_:
                            fields_.append(f)
                    fields = fields_
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
                        if isinstance(callable_, types.MethodType):
                            ret[field_name] = callable_(obj)
                        else:
                            ret[field_name] = callable_(obj.__class__, obj)
                    else:
                        ret[field_name] = getattr(obj, field_name) 
            return ret
    return simplejson.dumps(thing, cls=AEEncoder)


