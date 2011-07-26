#!/usr/bin/env python

from env_setup import setup
setup()

from agar.json import MultiPageHandler

from restler import serializers

from webapp2 import WSGIApplication, Route

from tests.models import Model1


V1_SERVICE_STRATEGY = serializers.ModelStrategy(Model1, include_all_fields=True)
V2_SERVICE_STRATEGY = V1_SERVICE_STRATEGY - ["boolean", "phonenumber"]


def create_sample_data():
    all = Model1.all().fetch(10)
    if len(all) < 10:
        model1 = Model1(string='test entry %s'% len(all))
        model1.put()

class V1ApiHandlerService(MultiPageHandler):
    def get(self):
        create_sample_data()
        return self.json_response(Model1.all(), V1_SERVICE_STRATEGY)

class V2ApiHandlerService(MultiPageHandler):
    def get(self):
        create_sample_data()
        return self.json_response(Model1.all(), V2_SERVICE_STRATEGY)

# Application
def get_application():
    from agar.env import on_production_server
    return WSGIApplication(
        [
            Route('/api/v1/model1', V1ApiHandlerService, name='api-v1'),
            Route('/api/v2/model1', V2ApiHandlerService, name='api-v2')
        ],
        debug=not on_production_server
    )
application = get_application()

def main():
    from google.appengine.ext.webapp import util
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
