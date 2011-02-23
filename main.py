#!/usr/bin/env python

from env_setup import setup
setup()

# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
# 
# from google.appengine.dist import use_library
# use_library('django', '1.2')

from hulk.env import on_production_server

from webapp2 import RequestHandler, WSGIApplication


class MainHandler(RequestHandler):
    def get(self):
        html = """
        <html>
            <body>
              <ul>
                <li><a href="/lib_config">lib_config settings</a></li>
                <li><a href="/api/v1/model1">/api/v1/model1</a></li>
                <li><a href="/api/v2/model1">/api/v2/model1</a></li>
              </ul>
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
