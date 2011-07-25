"""
The ``agar.url`` module contains classes to help working with application-wide URLs.
"""

from google.appengine.api import lib_config

from agar.env import on_production_server


class ConfigDefaults(object):
    """
    :py:class:`~agar.config.Config` settings for the ``agar.url`` library.
    Settings are under the ``agar_url`` namespace.

    The following settings (and defaults) are provided::

        agar_url_DEBUG = False
        agar_url_PRODUCTION_DOMAIN = ''
        agar_url_APPLICATIONS = ['main']

    To override ``agar.url`` settings, define values in the ``appengine_config.py`` file in the root of your app.
    """
    DEBUG = False
    PRODUCTION_DOMAIN = ''
    APPLICATIONS = ['main']

#: The configuration object for ``agar.url`` settings.
config = lib_config.register('agar_url', ConfigDefaults.__dict__)

def url_for(name, *args, **kwargs):
    # todo throw exception if no url found?
    owned_domain = kwargs.pop('owned_domain', True)
    request = kwargs.pop('request')
    _full = kwargs.get('_full', False)
    _netloc = kwargs.get('_netloc')
    if _netloc is None and _full and owned_domain and config.PRODUCTION_DOMAIN and on_production_server:
        kwargs['_netloc'] = config.PRODUCTION_DOMAIN
    if owned_domain and _full:
        kwargs['_scheme'] = 'http'
    url = None
    for app_name in config.APPLICATIONS:
        app_module = __import__(app_name)
        try:
            application = app_module.application
            url = application.router.build(name, request, args, kwargs)
            if url is not None:
                break
        except KeyError:
            pass
    return url
