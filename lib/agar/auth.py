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
    """
    An ``authenticator`` for use with the :py:func:`agar.auth.authentication_required` decorator. Enforces that a request
    was made via HTTPS.  If it was a secure request, it will defer to the ``agar_auth_authenticate`` configured function.  If not, it will
    return ``None``.
    """
    import urlparse
    from agar.env import on_server
    scheme, netloc, path, query, fragment = urlparse.urlsplit(request.url)
    if on_server and scheme and scheme.lower() != 'https':
        return None
    return config.authenticate(request)

def authentication_required(authenticator=None):
    """
    A decorator to authenticate a `RequestHandler <http://webapp-improved.appspot.com/api.html#webapp2.RequestHandler>`_ method.
    If the ``authenticator`` function returns a non-``None`` value, it will place that value on the request under the
    variable ``account`` so that the handler can access it. If the ``authenticator`` function returns ``None``, it will
    `abort <http://webapp-improved.appspot.com/api.html#webapp2.RequestHandler.abort>`_ the call with a status of ``403``.
    """
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
    """
    A decorator to authenticate a secure request to a `RequestHandler <http://webapp-improved.appspot.com/api.html#webapp2.RequestHandler>`_ method.
    This decorator uses the :py:func:`agar.auth.authenticate_https` ``authenticator``.
    """
    return authentication_required(authenticator=authenticate_https)
