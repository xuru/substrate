#!/usr/bin/env python

from setup import setup

from hulk.json import MultiPageHandler

from restler import serializers

from webapp2 import WSGIApplication

from models import Model1


V1_SERVICE_STRATEGY = serializers.ModelStrategy(Model1)
V2_SERVICE_STRATEGY = V1_SERVICE_STRATEGY + ["boolean", "phonenumber"]

class V1ApiHandlerService(MultiPageHandler):
    def get(self):
        return self.json_response(Model1.all(), V1_SERVICE_STRATEGY)

class V2ApiHandlerService(MultiPageHandler):
    def get(self):
        return self.json_response(Model1.all(), V2_SERVICE_STRATEGY)

# Application
def get_application():
    from hulk.env import on_production_server
    return WSGIApplication(
        [
            ('/api/v1/model1', V1ApiHandlerService),
            ('/api/v2/model1', V2ApiHandlerService)
        ],
        debug=not on_production_server
    )
application = get_application()

def main():
    from google.appengine.ext.webapp import util
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
