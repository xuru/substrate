#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys, os

from google.appengine.api import apiproxy_stub_map

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from webapp2 import WSGIApplication


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

def url_for(name, *args, **kwargs):
    from main import application as main_application
    owned_domain = kwargs.pop('owned_domain', True)
    request = kwargs.pop('request', None)
    _full = kwargs.get('_full', False)
    _netloc = kwargs.get('_netloc', None)
    if _netloc is None and _full and owned_domain and on_production_server:
        kwargs['_netloc'] = main_application.config.get_config('main', key='PRODUCTION_DOMAIN', default=[])
    if owned_domain:
        kwargs['_scheme'] = 'http'
    url = None
    APPLICATIONS = main_application.config.get_config('main', key='APPLICATIONS', default=[])
    for app_name in APPLICATIONS:
        app_module = __import__(app_name)
        try:
            application = app_module.application
            url = application.router.build(name, request, args, kwargs)
            if url is not None:
                break
        except KeyError:
            pass
    return url


class MainHandler(webapp.RequestHandler):
    def get(self):
        html = """
        <html>
            <body>
                <ul>
                    <li> <a href="/api/v1/model1">V1 API</a> </li>
                    <li> <a href="/api/v2/model1">V2 API</a> </li>
                </ul>
            </body>
        </html>
        """
        self.response.out.write(html)

# Configuration
def load_config_module(m):
    config = {}
    for key in m.__dict__:
        if not key.startswith('__'):
            config[key] = m.__dict__[key]
    return config

import main_config
config = {
    'main': load_config_module(main_config)
}

def get_application():
    return WSGIApplication([('/', MainHandler)], config=config, debug=not on_production_server)
application = get_application()

def main():
    from google.appengine.ext.webapp import util
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
