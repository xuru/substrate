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
from lib.ext.env import load_config_module

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from webapp2 import RequestHandler, WSGIApplication



class MainHandler(RequestHandler):
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
#def load_config_module(m):
#    config = {}
#    for key in m.__dict__:
#        if not key.startswith('__'):
#            config[key] = m.__dict__[key]
#    return config

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
