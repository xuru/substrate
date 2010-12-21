#!/usr/bin/env python

from setup import setup
setup()

from hulk.env import on_production_server

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
