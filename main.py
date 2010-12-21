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

from setup import setup
setup()

from hulk.env import load_config_module, on_production_server

from webapp2 import RequestHandler, WSGIApplication


class MainHandler(RequestHandler):
    def get(self):
        html = """
        <html>
            <body>
                Hello World!
            </body>
        </html>
        """
        self.response.out.write(html)

def get_application():
    return WSGIApplication([('/', MainHandler)], debug=not on_production_server)
application = get_application()

def main():
    from google.appengine.ext.webapp import util
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
