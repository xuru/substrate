import os

from google.appengine.api import apiproxy_stub_map

have_appserver = bool(apiproxy_stub_map.apiproxy.GetStub('datastore_v3'))

# Get the appid
appid = None
if have_appserver:
    appid = os.environ.get('APPLICATION_ID')
else:
    try:
        from google.appengine.tools import dev_appserver
        from aecmd import PROJECT_DIR
        appconfig, unused = dev_appserver.LoadAppConfig(PROJECT_DIR, {})
        appid = appconfig.application
    except ImportError:
        appid = None

# Are we running on a google server?
on_server = have_appserver and appid and not os.environ.get('SERVER_SOFTWARE', '').lower().startswith('devel')
# Are we running on an integration environment?
on_integration_server = on_server and appid.lower().endswith('-int')
# Are we running on a production environment?
on_production_server = on_server and not on_integration_server


def load_config_module(m):
    config = {}
    for key in m.__dict__:
        if not key.startswith('__'):
            config[key] = m.__dict__[key]
    return config