
import sys, os
import logging

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util

from restler import serializers


def render_to_json(response, model_or_query, strategy=None):
    json = serializers.to_json(model_or_query, strategy)
    response.set_status(200)
    response.headers['Content-Type'] = "application/json"
    response.out.write(resp)

class RestlerApp(webapp.WSGIApplication):

    def __init__(self, url_mapping, debug=False):
        """Initializes this application with the given URL mapping.

        Args:
        url_mapping: list of (URI regular expression, RequestHandler) pairs
                    (e.g., [('/', ReqHan)])
        debug: if true, we send Python stack traces to the browser on errors
        """
        self._init_url_mappings(url_mapping)
        self.__debug = debug
        RestlerApp.active_instance = self
        self.current_request_args = ()
    
    def __call__(self, environ, start_response):
        logging.info("App called")
        """Called by WSGI when a request comes in."""
        request = self.REQUEST_CLASS(environ)
        response = self.RESPONSE_CLASS()

        RestlerApp.active_instance = self

        handler = None
        groups = ()
        for regexp, handler_class in self._url_mapping:
            match = regexp.match(request.path)
            if match:
                handler = handler_class()
                handler.initialize(request, response)
                groups = match.groups()
                break

        self.current_request_args = groups

        resp = None
        if handler:
            try:
                method = environ['REQUEST_METHOD']
                logging.info(method)
                if method == 'GET':
                    resp = handler.get(*groups)
                elif method == 'POST':
                    resp = handler.post(*groups)
                elif method == 'HEAD':
                    resp = handler.head(*groups)
                elif method == 'OPTIONS':
                    resp = handler.options(*groups)
                elif method == 'PUT':
                    resp = handler.put(*groups)
                elif method == 'DELETE':
                    resp = handler.delete(*groups)
                elif method == 'TRACE':
                    resp = handler.trace(*groups)
                else:
                    handler.error(501)
                if isinstance(resp, (db.Model, db.Query)):
                    resp = serializers.to_json(resp)
                elif resp and (isinstance(resp, tuple)):
                    logging.info("serializing")
                    resp = serializers.to_json(*resp)
                if resp:
                    logging.info("resp=" + str(resp))
                    response.set_status(200)
                    response.headers['Content-Type'] = "application/json"
                    response.out.write(resp)
                else:
                    logging.info("No response!")
            except Exception, e:
                handler.handle_exception(e, self.__debug)
        else:
            response.set_status(404)

        response.wsgi_write(start_response)
        return ['']

