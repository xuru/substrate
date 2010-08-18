
from google.appengine.ext import db
from django.utils import simplejson


def to_json(thing, serialization_mapper={}):
    class AEEncoder(simplejson.JSONEncoder):
        def default(self, obj):
            ret = {}
            if isinstance(obj, db.Model):
                if serialization_mapper is None:
                    fields = obj.properties().keys() 
                else:
                    fields = ( serialization_mapper.get(obj.__class__, []) 
                            or getattr(obj, "__serialize__", []) 
                            or obj.properties().keys() )
                # if any fields use the "-" to exclude a field from 'all' properties
                if not isinstance(fields, (tuple, list)): 
                    fields = [fields]
                if any([f.startswith("-") for f in fields]):
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

                for field_name in fields:
                    field = getattr(obj, field_name, None)
                    if not field:
                        raise ValueError( "'%s' isn't a valid property of %s" 
                                        % (f, obj.__class__.__name__))
                    if callable(field):
                        if field.__name__ in ["key", "kind", "parent", "parent_key"]:
                            ret[field_name] = None if field() is None else str(field())
                        else:
                            ret[field_name] = field(obj)
                    else:
                        ret[field_name] = getattr(obj, field_name) 
            if isinstance(obj, db.Query):
                return [o for o in obj]
            return ret
    return simplejson.dumps(thing, cls=AEEncoder)


