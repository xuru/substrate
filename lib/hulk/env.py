import os

from google.appengine.api import apiproxy_stub_map, lib_config

class ConfigDefaults(object):
    """Configurable constants.

    To override hulk.env configuration values, define values like this
    in your appengine_config.py file (in the root of your app):

        hulk_env_INTEGRATION_APP_ID = 'other_int_id'
        hulk_env_PRODUCTION_APP_ID = 'other_prod_id'
    """
    INTEGRATION_APP_ID = ''
    PRODUCTION_APP_ID = ''

config = lib_config.register('hulk_env', ConfigDefaults.__dict__)


server_software = os.environ.get('SERVER_SOFTWARE', '')
have_appserver = bool(apiproxy_stub_map.apiproxy.GetStub('datastore_v3'))

# Get the appid
appid = None
if have_appserver:
    appid = os.environ.get('APPLICATION_ID')
else:
    try:
        project_dir = os.path.dirname(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
        from google.appengine.tools import dev_appserver
        appconfig, unused = dev_appserver.LoadAppConfig(project_dir, {})
        appid = appconfig.application
    except ImportError:
        appid = None

# Are we running on the dev server?
on_development_server = have_appserver and server_software.lower().startswith('devel')
# Are we running on a google server?
on_server = bool(have_appserver and appid and server_software and not on_development_server)
# Are we running on an integration environment?
on_integration_server = on_server and appid.lower().endswith('-int') or appid.lower() == config.INTEGRATION_APP_ID.lower()
# Are we running on a production environment?
on_production_server = on_server and not on_integration_server or appid.lower() == config.PRODUCTION_APP_ID.lower()
