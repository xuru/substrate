import os

from google.appengine.api import apiproxy_stub_map


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
on_integration_server = on_server and appid.lower().endswith('-int')
# Are we running on a production environment?
on_production_server = on_server and not on_integration_server

import logging
logging.info("have_appserver: %s" % have_appserver)
logging.info("appid: %s" % appid)
logging.info("server_software: %s" % server_software)
logging.info("on_server: %s" % on_server)
logging.info("on_development_server: %s" % on_development_server)
logging.info("on_integration_server: %s" % on_integration_server)
logging.info("on_production_server: %s" % on_production_server)
