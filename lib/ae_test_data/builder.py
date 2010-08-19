import handlers
import logging
import re

def _convert(name):
    # http://stackoverflow.com/questions/1175208/does-the-python-standard-library-have-function-to-convert-camelcase-to-camel-case
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def _populate_instance(cls, *args, **kwargs):
    # TODO throw exception if has args? or just remove from sig
    params = {}
    properties = cls.properties()
    
    for key in kwargs:
        if key in properties:
            del properties[key]
        
    for name, value in properties.items():
        if value.required:
            if value.default is not None:
                params[name] = value.default
            else:
                try:
                    property_handler = getattr(handlers, _convert(value.__class__.__name__))
                    property_handler(params, name)
                except AttributeError, e:
                    logging.info(e)
                    return None
    
    params.update(kwargs)
    return cls(**params)


def build(cls, *args, **kwargs):
    instance = _populate_instance(cls, *args, **kwargs)
    instance.put()
    return instance

def build_without_save(cls, *args, **kwargs):
    return _populate_instance(cls, *args, **kwargs)
    
def lazy_build(cls, *args, **kwargs):
    raise Exception("Not Implemented.")

def create(cls, *args, **kwargs):
    # call .create or use lib for key_name
    # could be a param on builder(cls, *args, **kwargs, use_key_name=False)
    # call create() if exists?
    raise Exception("Not Implemented.")

