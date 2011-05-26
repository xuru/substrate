from agar.config import Config


class AuthConfig(Config):
    """
    :py:class:`~agar.config.Config` settings for the ``agar.auth`` library.
    Settings are under the ``agar_auth`` namespace.

    The following settings (and defaults) are provided::

        def agar_auth_authenticate(request):
            return None

    To override ``agar.auth`` settings, define values in the ``appengine_config.py`` file in the root of your app.
    """
    _namepace = 'agar_auth'

    def authenticate(request):
        """
        The authenticate function. It takes a single `Request <http://webapp-improved.appspot.com/api.html#webapp2.Request>`_
        argument, and returns a non-``None`` value if the request can be authenticated. If the request can not be
        authenticated, the function should return ``None``. The type of the returned value can be anything, but it
        should be a type that your `RequestHandler <http://webapp-improved.appspot.com/api.html#webapp2.RequestHandler>`_ expects.
        The default implementation always returns ``None``.
        """
        return None

#: The configuration object for ``agar.auth`` settings.
config = AuthConfig.get_config()

def authenticate_https(request):
    """
    An authenticate function for use with the :py:func:`agar.auth.https_authentication_required` decorator. Enforces that a request
    was made via HTTPS.  If it was a secure request, it will defer to the config function :py:meth:`~agar.auth.AuthConfig.authenticate`.
    If not, it will return ``None``.
    """
    import urlparse
    from agar.env import on_server
    scheme, netloc, path, query, fragment = urlparse.urlsplit(request.url)
    if on_server and scheme and scheme.lower() != 'https':
        return None
    return config.authenticate(request)

def authentication_required(authenticate=None):
    """
    A decorator to authenticate a `RequestHandler <http://webapp-improved.appspot.com/api.html#webapp2.RequestHandler>`_ method.
    If the authenticate function returns a non-``None`` value, it will place that value on the request under the
    variable ``account`` so that the handler can access it. If the authenticate function returns ``None``, it will
    `abort <http://webapp-improved.appspot.com/api.html#webapp2.RequestHandler.abort>`_ the call with a status of ``403``.

    Keyword arguments:
        ``authenticate`` -- The authenticate function to use to authenticate a request. The function should take a single
        `Request <http://webapp-improved.appspot.com/api.html#webapp2.Request>`_
        argument, and return a non-``None`` value if the request can be authenticated. If the request can not be
        authenticated, the function should return ``None``. The type of the returned value can be anything, but it
        should be a type that your `RequestHandler <http://webapp-improved.appspot.com/api.html#webapp2.RequestHandler>`_
        expects. If ``None``, the config function :py:meth:`~agar.auth.AuthConfig.authenticate` will be used.
    """
    if authenticate is None:
        authenticate = config.authenticate
    def decorator(request_method):
        def wrapped(self, *args, **kwargs):
            account = authenticate(self.request)
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
    This decorator uses the :py:func:`~agar.auth.authenticate_https` authentication function.
    """
    return authentication_required(authenticate=authenticate_https)
