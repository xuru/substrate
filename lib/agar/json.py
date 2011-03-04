import copy
import datetime
import logging

from google.appengine.api import lib_config
from google.appengine.ext.db import BadRequestError, BadValueError

from agar.models import ModelException

from pytz.gae import pytz

from restler.serializers import json_response as restler_json_response

from webapp2 import RequestHandler, HTTPException


class ConfigDefaults(object):
    """Configurable constants.

    To override agar.json configuration values, define values like this
    in your appengine_config.py file (in the root of your app):

        agar_json_DEBUG = True
        agar_json_DEFAULT_PAGE_SIZE = 20
        agar_json_MAX_PAGE_SIZE = 200
    """
    DEBUG = False
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    USE_DATA_ROOT_NODE = True

config = lib_config.register('agar_json', ConfigDefaults.__dict__)


def string_to_int(s, default=10):
    try:
        return int(s)
    except:
        return default

class JsonRequestHandler(RequestHandler):
    """A RequestHandler class to help with json web service handlers, including error handling"""
    def _setup_context(self, context):
        if not context:
            context = {}
        context['request'] = self.request
        return context
    
    def _setup_data(self, model_or_query, status_code, status_text):
        data = dict()
        data['status_code'] = status_code
        data['status_text'] = status_text
        data['timestamp'] = datetime.datetime.now(pytz.utc)
        if config.USE_DATA_ROOT_NODE:
            data['data'] = model_or_query
        else:    
            data.update(model_or_query)
        return data

    def json_response(self, model_or_query, strategy=None, status_code=200, status_text='OK', context=None):
        context = self._setup_context(context)
        data = self._setup_data(model_or_query, status_code, status_text)

        return restler_json_response(self.response, data, strategy=strategy, status_code=status_code, context=context)

    def handle_exception(self, exception, debug_mode):
        status_text = exception.message
        if isinstance(exception, HTTPException):
            code = exception.code
        elif isinstance(exception, ModelException):
            code = 400
            status_text = "BAD_REQUEST: %s" % status_text
        else:
            code = 500
            status_text = "INTERNAL_SERVER_ERROR: %s" % status_text
            logging.error("API 500 ERROR: %s" % exception)
        if code == 401:
            status_text = 'UNAUTHORIZED'
        if code == 403:
            status_text = 'FORBIDDEN'
        if code == 404:
            status_text = 'NOT_FOUND'
        if code == 405:
            status_text = 'METHOD_NOT_ALLOWED'
        if code == 400:
            logging.warning("API %s WARNING: %s" % (code, status_text))
        return self.json_response({}, status_code=code, status_text=status_text)

class MultiPageHandler(JsonRequestHandler):
    """A RequestHandler class to help with 'page_size' and 'cursor' parsing and logic"""
    @property
    def page_size(self):
        page_size = string_to_int(self.request.get('page_size', str(config.DEFAULT_PAGE_SIZE)))
        page_size = min(max(page_size, 1), config.MAX_PAGE_SIZE)
        return page_size

    def fetch_page(self, query):
        original_query = copy.deepcopy(query)
        cursor = self.request.get('cursor', None)
        if cursor is not None:
            try:
                query = query.with_cursor(cursor)
            except (BadValueError, BadRequestError):
                query = original_query
        try:
            results = query.fetch(self.page_size)
        except (BadValueError, BadRequestError):
#            self.abort(500, "BAD_REQUEST: The cursor has expired (%s)" % cursor)
            if cursor is not None:
                query = original_query
                results = query.fetch(self.page_size)
            else:
                raise
        next_page_key = None
        if len(results) == self.page_size:
            next_page_key = query.cursor()
        return results, next_page_key


class CorsMultiPageHandler(MultiPageHandler):
    """ A RequestHandler to help with json, multi-page requests and Cross-Origin Resource sharing  """
    def options(self):
        origin = self.request.headers.get('Origin', 'unknown origin')
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE, OPTIONS'
        self.response.headers['Access-Control-Max-Age'] = 1728000 
        self.response.headers['Access-Control-Allow-Credentials'] = \
            self.request.headers.get('Access-Credentials', 'true')
        self.response.headers['Access-Control-Allow-Origin']= ':'.join(origin.split(':')[0:2])
        self.response.headers['Access-Control-Allow-Origin']= origin.strip()
        self.response.headers['Access-Control-Allow-Headers'] = \
            self.request.headers.get('Access-Control-Request-Headers', '') 

    """A RequestHandler class to help with json web service handlers, including error handling"""
    def json_response(self, model_or_query, strategy=None, status_code=200, status_text='OK', context=None):       
        context = self._setup_context(context)
        data = self._setup_data(model_or_query, status_code, status_text)

        origin = self.request.headers.get('Origin', '') 
        if origin:
            self.response.headers['Access-Control-Allow-Origin'] = origin
        else:
            self.response.headers['Access-Control-Allow-Origin'] = "/".join(self.request.headers.get("Referer", "").split("/")[0:3]) 
        self.response.headers['Access-Control-Allow-Headers'] = "true"
        self.response.headers['Access-Control-Allow-Credentials'] = "true"

        return restler_json_response(self.response, data, strategy=strategy, status_code=status_code, context=context)

