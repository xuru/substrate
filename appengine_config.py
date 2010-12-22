##############################################################################
# GOOGLE SETTINGS
##############################################################################

# If your application uses Django and requires a specific version of
# Django, uncomment the following block of three lines.  Currently
# supported values for the Django version are '0.96' (the default),
# '1.0', and '1.1'.

from google.appengine.dist import use_library
#use_library('django', '1.0')
#import django


##############################################################################
# HULK SETTINGS
##############################################################################

# Root level WSGI application modules that 'url_for' will search
hulk_url_APPLICATIONS = ['main', 'api']

# Enable debug logging for the hulk.url module
#hulk_url_DEBUG = False

# When calling 'url_for' with _full=True and owned_domain=True,
# use this value for the URL host when hulk.env.on_production_server == True
#hulk_url_PRODUCTION_DOMAIN = 'www.mydomain.com'

# Enable debug logging for the hulk.auth module
#hulk_auth_DEBUG = False

# Default static API keys for use with the default 'authorize' method
#hulk_auth_VALID_API_KEYS = ['key1', 'key2']

# The authorization function to use
#hulk_auth_authorize = lambda handler, *args, **kwargs: return True

# Enable debug logging for the hulk.json module
#hulk_json_DEBUG = False

# The default number of results to return per 'page'
#hulk_json_DEFAULT_PAGE_SIZE = 10

# The maximum number of results to return per 'page', regardless of how many are requested
#hulk_json_MAX_PAGE_SIZE = 100
