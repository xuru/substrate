import env_setup; env_setup.setup(); env_setup.setup_django()

from webapp2 import WSGIApplication, RequestHandler, Route

from agar.env import on_production_server


class WarmupHandler(RequestHandler):
    def get(self):
        self.response.out.write("Warmed Up")


def get_application():
    return WSGIApplication(
        [
            #Documentation
            Route('/_ah/warmup', handler=WarmupHandler, name='warmup'),
        ],
        debug=not on_production_server
    )
application = get_application()


def main():
    from google.appengine.ext.webapp import util
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
