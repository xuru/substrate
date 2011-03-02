import logging
import re
import string

from datetime import date, datetime, time
from random import choice, randint, random, uniform

from google.appengine.api import lib_config
from google.appengine.api.users import User
from google.appengine.ext import db


class ConfigDefaults(object):
    """Configurable constants.

    To override builder configuration values, define values like this
    in your appengine_config.py file (in the root of your app):

        builder_STRING_LENGTH = 4
        builder_DEFAULT_CONSTRUCTOR = 'create_new_entity'
    """
    
    BLOB_LENGTH = 6
    BYTE_STRING_LENGTH = 6
    DOMAIN_LENGTH = 8
    FLOAT_MIN_RANGE = 0
    FLOAT_MAX_RANGE = 100
    INT_MIN_RANGE = 0
    INT_MAX_RANGE = 100000
    STRING_LENGTH = 6
    
    DEFAULT_CONSTRUCTOR = None
    
    def blob_property(_property):
        value = ''.join([choice(string.ascii_letters + string.digits) for i in xrange(config.BLOB_LENGTH)])
        if len(value) > 0:
            return '%s_%s'% (_property.name, value)
        else:
            return _property.name
    
    def byte_string_property(_property):
        value = ''.join([choice(string.ascii_letters + string.digits) for i in xrange(config.BYTE_STRING_LENGTH)])
        if len(value) > 0:
            return '%s_%s'% (_property.name, value)
        else:
            return _property.name

    def boolean_property(_property):
        if random() < .5:
            return True
        else:
            return False
    
    def category_property(_property):
        return _property.name

    def date_property(_property):
        return date(1970, 1, 1)
    
    def date_time_property(_property):
        return datetime(1970, 1, 1, 0, 0)
    
    def email_property(_property):
        value = ''.join([choice(string.ascii_letters + string.digits) for i in xrange(config.DOMAIN_LENGTH)])
        return '%s@%s.com'% (_property.name, value)

    def float_property(_property):
        return uniform(config.FLOAT_MIN_RANGE, config.FLOAT_MAX_RANGE)
    
    def geo_pt_property(_property):
        # lat & lon of Mpls, MN
        return db.GeoPt(44.88, lon=93.22)
    
    def im_property(_property):
        return db.IM('http://talk.google.com/', 'gtalk_user')

    def integer_property(_property):
        return randint(config.INT_MIN_RANGE, config.INT_MAX_RANGE)
    
    def link_property(_property):
        return db.Link('http://www.domain.com')
    
    def phone_number_property(_property):
        return db.PhoneNumber('(612) 555-1234')

    def postal_address_property(_property):
       return db.PostalAddress('123 Main Street, Minneapolis, MN')

    def rating_property(_property):
        return db.Rating(50)

    def string_property(_property):
        value = ''.join([choice(string.ascii_letters + string.digits) for i in xrange(config.STRING_LENGTH)])
        if len(value) > 0:
            return '%s_%s'% (_property.name, value)
        else:
            return _property.name
    
    def text_property(_property):
        return _property.name

    def time_property(_property):
        return time(12, 0, 0)

    def user_property(_property):
        return User('user@gmail.com')


config = lib_config.register('builder', ConfigDefaults.__dict__)



def _convert(name):
    # http://stackoverflow.com/questions/1175208/does-the-python-standard-library-have-function-to-convert-camelcase-to-camel-case
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def _populate_instance(cls, *args, **kwargs):
    # TODO throw exception if has args? or just remove from sig
    required_only = kwargs.get('required_only', True)
    constructor = kwargs.get('constructor')
    if constructor: del kwargs['constructor']
    
    params = {}
    cls_properties = cls.properties()
    
    # don't create data for passed in params
    for key in kwargs:
        if key in cls_properties:
            del cls_properties[key]

    for _property in cls_properties.values():
        if _property.required or not required_only:
            if _property.default is not None:
                params[_property.name] = _property.default_value()
            else:
                try:
                    property_config_name = _convert(_property.__class__.__name__)
                    property_config_function = config.__getattr__(property_config_name)
                    params[_property.name] = property_config_function(_property)
                except AttributeError, e:
                    logging.info(e)
                    return
    
    params.update(kwargs)
    if constructor is None and config.DEFAULT_CONSTRUCTOR is None:
        return cls(**params)
    else:
        if constructor is not None:
            _constructor = getattr(cls, constructor)
        elif config.DEFAULT_CONSTRUCTOR is not None:
            _constructor = getattr(cls, config.DEFAULT_CONSTRUCTOR)
        else:
            # no constructor set, use class constuctor
            return cls(**params)
        return _constructor(**params)


def build(cls, *args, **kwargs):
    instance = _populate_instance(cls, *args, **kwargs)
    if not instance.is_saved():
        instance.put()
    return instance




