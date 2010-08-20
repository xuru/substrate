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
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util

from restler import serializers
from restler.webapp import RestlerApp


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')


from models import Model1

V1_SERVICE_STRATEGY = serializers.ModelStrategy(Model1)
V2_SERVICE_STRATEGY = V1_SERVICE_STRATEGY + ["boolean", "phonenumber"]

class V1ApiHandlerService(webapp.RequestHandler):
    def get(self):
        return Model1.all()

class V2ApiHandlerService(webapp.RequestHandler):
    def get(self):
        return Model1.all(), V2_SERVICE_STRATEGY

def main():
    application = RestlerApp([('/api/v1/model1', V1ApiHandlerService),
                              ('/api/v2/model1', V2ApiHandlerService)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
