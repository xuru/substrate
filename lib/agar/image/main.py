#!/usr/bin/env python

def get_application():
    from google.appengine.api import lib_config
    from agar.image import ConfigDefaults
    config = lib_config.register('agar_image', ConfigDefaults.__dict__)
    from google.appengine.ext.webapp import WSGIApplication
    return WSGIApplication(
        [
            (config.UPLOAD_URL, config.UPLOAD_HANDLER),
        ],
        debug=True
    )
application = get_application()

def main():
    from google.appengine.ext.webapp import util
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
