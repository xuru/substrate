from urlparse import urlparse

from google.appengine.api import lib_config

from hulk.env import on_production_server


class ConfigDefaults(object):
    """Configurable constants.

    To override hulk.auth configuration values, define values like this
    in your appengine_config.py file (in the root of your app):

        hulk_auth_DEBUG = True
        hulk_auth_VALID_API_KEYS = ['key1', 'key2']
        hulk_auth_authorize = lambda handler, *args, **kwargs: return True
    """
    DEBUG = False

    if on_production_server:
        VALID_API_KEYS = ['prodapikey1', 'prodapikey1']
    else:
        VALID_API_KEYS = ['testapikey1', 'testapikey2']

    def authorize(handler, *args, **kwargs):
        from hulk.env import on_production_server
        scheme, netloc, path, query, fragment = urlparse.urlsplit(handler.request.url)
        # Only allow HTTPS on PRODuction
        if on_production_server and scheme and scheme.lower() != 'https':
            return False
        api_key = handler.request.get('api_key', default_value=None)
        valid_api_keys = config.VALID_API_KEYS
        return api_key in valid_api_keys

config = lib_config.register('hulk_auth', ConfigDefaults.__dict__)

def api_key_required(method, auth_func=None):
    def authorized_method(handler, *args, **kwargs):
        if auth_func is None:
            auth_func = config.authorize
        if auth_func(handler, *args, **kwargs):
            method(handler, *args, **kwargs)
        else:
            handler.abort(401)
    return authorized_method
