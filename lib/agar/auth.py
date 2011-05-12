from google.appengine.api import lib_config


class ConfigDefaults(object):
    """Configurable constants.

    To override agar.auth configuration values, define values like this
    in your appengine_config.py file (in the root of your app):

        agar_auth_DEBUG = True
        agar_auth_authenticate = lambda request, *args, **kwargs: return None
    """
    DEBUG = False

    def authenticate(request):
        return None

config = lib_config.register('agar_auth', ConfigDefaults.__dict__)


def authenticate_https(request):
    import urlparse
    from agar.env import on_server
    scheme, netloc, path, query, fragment = urlparse.urlsplit(request.url)
    if on_server and scheme and scheme.lower() != 'https':
        return None
    return config.authenticate(request)

def authentication_required(authenticator=None):
    if authenticator is None:
        authenticator = config.authenticate
    def decorator(request_method):
        def wrapped(self, *args, **kwargs):
            account = authenticator(self.request)
            if account is not None:
                self.request.account = account
                request_method(self, *args, **kwargs)
            else:
                self.abort(403)
        return wrapped
    return decorator

def https_authentication_required():
    return authentication_required(authenticator=authenticate_https)
