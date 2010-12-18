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
import urlparse
from google.appengine.api.datastore_errors import BadRequestError
from lib.ext.json import MultiPageHandler, MultiPageHandler

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from restler import serializers
from restler.serializers import json_response as restler_json_response
from webapp2 import RequestHandler, WSGIApplication, HTTPException

from models import Model1, ModelException


V1_SERVICE_STRATEGY = serializers.ModelStrategy(Model1)
V2_SERVICE_STRATEGY = V1_SERVICE_STRATEGY + ["boolean", "phonenumber"]

OK = 'OK'
CREATED = 'CREATED'
BAD_REQUEST = 'BAD_REQUEST'
METHOD_NOT_ALLOWED = 'METHOD_NOT_ALLOWED'
UNAUTHORIZED = 'UNAUTHORIZED'
NOT_FOUND = 'NOT_FOUND'
INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'

# Utils
def string_to_int(s, default=10):
    try:
        return int(s)
    except:
        return default

# Authorization
def authorize(request):
    from main import on_production_server
    scheme, netloc, path, query, fragment = urlparse.urlsplit(request.url)
    # Only allow HTTPS on PRODuction
    if on_production_server and scheme and scheme.lower() != 'https':
        return False
    api_key = request.get('api_key', default_value=None)
    VALID_API_KEYS = application.config.get_config('api', key='VALID_API_KEYS', default=None)
    return api_key in VALID_API_KEYS

def authorization_required(method):
    def authorized_method(handler, *args, **kwargs):
        if authorize(handler.request):
            method(handler, *args, **kwargs)
        else:
            handler.abort(401)
    return authorized_method

## JSON Handler Base Class
#class JsonRequestHandler(RequestHandler):
#    def json_response(self, model_or_query, strategy=None, status_code=200, status_text='OK', context=None):
#        if not context:
#            context = {}
#        context['request'] = self.request
#        data = dict()
#        data['status_code'] = status_code
#        data['status_text'] = status_text
#        data['data'] = model_or_query
#        return restler_json_response(self.response, data, strategy=strategy, status_code=status_code, context=context)
#
#    def handle_exception(self, exception, debug_mode):
#        status_text = exception.message
#        if isinstance(exception, HTTPException):
#            code = exception.code
#        elif isinstance(exception, ModelException):
#            code = 400
#            status_text = "%s: %s" % (BAD_REQUEST, status_text)
#        else:
#            code = 500
#            status_text = "%s: %s" % (INTERNAL_SERVER_ERROR, status_text)
#            if debug_mode:
#                logging.error("INTERNAL_SERVER_ERROR %s: %s" % (code, status_text))
#        if code == 401:
#            status_text = UNAUTHORIZED
#        if code == 404:
#            status_text = NOT_FOUND
#        if code == 405:
#            status_text = METHOD_NOT_ALLOWED
#        return self.json_response({}, status_code=code, status_text=status_text)
#
## A RequestHandler class to help with 'page_size' and 'page_key' parsing and logic
#class MultiPageHandler(JsonRequestHandler):
#    @property
#    def page_size(self):
#        DEFAULT_PAGE_SIZE = application.config.get_config('api', key='DEFAULT_PAGE_SIZE', default=10)
#        MAX_PAGE_SIZE = application.config.get_config('api', key='MAX_PAGE_SIZE', default=100)
#        page_size = string_to_int(self.request.get('page_size', str(DEFAULT_PAGE_SIZE)))
#        page_size = min(max(page_size, 1), MAX_PAGE_SIZE)
#        return page_size
#
#    def fetch_page(self, query):
#        cursor = self.request.get('page_key', None)
#        if cursor is not None:
#            try:
#                query = query.with_cursor(cursor)
#            except BadRequestError:
#                self.abort(400, "The 'page_key' has expired: %s" % cursor)
#        results = query.fetch(self.page_size)
#        next_page_key = None
#        if len(results) == self.page_size:
#            next_page_key = query.cursor()
#        return results, next_page_key

class V1ApiHandlerService(MultiPageHandler):
    def get(self):
        return self.json_response(Model1.all(), V1_SERVICE_STRATEGY)

class V2ApiHandlerService(MultiPageHandler):
    def get(self):
        return self.json_response(Model1.all(), V2_SERVICE_STRATEGY)


from main import load_config_module
import api_config
config = {
    'api': load_config_module(api_config)
}

# Application
def get_application():
    from main import on_production_server
    return WSGIApplication(
        [
            ('/api/v1/model1', V1ApiHandlerService),
            ('/api/v2/model1', V2ApiHandlerService)
        ],
        config=config,
        debug=not on_production_server
    )
application = get_application()

def main():
    from google.appengine.ext.webapp import util
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
