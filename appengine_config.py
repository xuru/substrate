"""
The configuration file used by :py:mod:`agar.config` implementations and other libraries using the
`google.appengine.api.lib_config`_. Configuration overrides go in this file.
"""

from env_setup import setup
setup()

##############################################################################
# AGAR SETTINGS
##############################################################################

# Root level WSGI application modules that 'agar.url.uri_for()' will search
agar_url_APPLICATIONS = ['main', 'api']

##############################################################################
# SESSION SETTINGS
##############################################################################

# create a SESSION_KEY
# import os
# os.urandom(64)

#SESSION_KEY="\xa9\x9bl\x99&\x19\xfe\x8d\xad\xc5\xa9\xef\x7f\xde4\x1a0\xa8nu\x9f\x0f\x81\x8e\xf1D\xde\x1bA\xfc\xf7io\xc8\xbb[\xe8W\xf7\xc3@\xf0\x06\xd8\x11!\x10\xb6\x93%\x03p\xd7\xa4\x8b'(vs\x82\x93\x93e\x06"
#def webapp_add_wsgi_middleware(app):
#    from gaesessions import SessionMiddleware
#    app = SessionMiddleware(app, cookie_key=SESSION_KEY)
#    return app
#
#
