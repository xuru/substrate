from google.appengine.ext import db

def boolean_property(params, name):
    params[name] = True

def category_property(params, name):
    params[name] = name

def date_property(params, name):
    from datetime import date
    params[name] = date(1970, 1, 1)

def date_time_property(params, name):
    from datetime import datetime
    params[name] = datetime(1970, 1, 1, 0, 0)

def email_property(params, name):
    params[name] = 'joe_smith@domain.com'

def float_property(params, name):
    params[name] = 1.5

def im_property(params, name):
    params[name] = db.IM('http://talk.google.com/', 'gtalk_user')

def integer_property(params, name):
    params[name] = 1

def geo_pt_property(params, name):
    # lat & lon of Mpls, MN
    params[name] = db.GeoPt(44.88, lon=93.22)

def link_property(params, name):
    params[name] = db.Link('http://www.domain.com')

def phone_number_property(params, name):
    params[name] = db.PhoneNumber('(612) 555-1234')

def postal_address_property(params, name):
    params[name] = db.PostalAddress('123 Main Street, Minneapolis, MN')

def rating_property(params, name):
    params[name] = db.Rating(50)

def string_property(params, name):
    params[name] = name

def string_list_property(params, name):
    # todo this prop is always default=[], so handler can be removed?
    params[name] = []

def text_property(params, name):
    params[name] = name

def time_property(params, name):
    from datetime import time
    params[name] = time(12, 0, 0)

def user_property(params, name):
    from google.appengine.api.users import User
    params[name] = User('user@gmail.com')
