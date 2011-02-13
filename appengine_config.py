##############################################################################
# GOOGLE SETTINGS
##############################################################################

# If your application uses Django and requires a specific version of
# Django, uncomment the following block of three lines.  Currently
# supported values for the Django version are '0.96' (the default),
# '1.0', and '1.1'.

# webapp_django_version = 1.1


##############################################################################
# HULK SETTINGS
##############################################################################

# Root level WSGI application modules that 'hulk.url.url_for()' will search
hulk_url_APPLICATIONS = ['main', 'api']

# The integration appid if it doesn't end in '-int'
# hulk_env_INTEGRATION_APP_ID = ''

# Enable debug logging for the hulk.url module
#hulk_url_DEBUG = False

# When calling 'url_for' with _full=True and owned_domain=True,
# use this value for the URL host when hulk.env.on_production_server == True
#hulk_url_PRODUCTION_DOMAIN = 'www.mydomain.com'

# Enable debug logging for the hulk.auth module
#hulk_auth_DEBUG = False

# Default static API keys for use with the default 'authorize' function
#hulk_auth_VALID_API_KEYS = ['key1', 'key2']

# The authorization function to use
#hulk_auth_authorize = lambda handler, *args, **kwargs: return True

# Enable debug logging for the hulk.json module
#hulk_json_DEBUG = False

# The default number of results to return per 'page'
#hulk_json_DEFAULT_PAGE_SIZE = 10

# The maximum number of results to return per 'page', regardless of how many are requested
#hulk_json_MAX_PAGE_SIZE = 100


##############################################################################
# SESSION SETTINGS
##############################################################################

# create a SESSION_KEY
# import os
# os.urandom(64)

SESSION_KEY="\xa9\x9bl\x99&\x19\xfe\x8d\xad\xc5\xa9\xef\x7f\xde4\x1a0\xa8nu\x9f\x0f\x81\x8e\xf1D\xde\x1bA\xfc\xf7io\xc8\xbb[\xe8W\xf7\xc3@\xf0\x06\xd8\x11!\x10\xb6\x93%\x03p\xd7\xa4\x8b'(vs\x82\x93\x93e\x06"
def webapp_add_wsgi_middleware(app):
    from gaesessions import SessionMiddleware
    app = SessionMiddleware(app, cookie_key=SESSION_KEY)
    return app


