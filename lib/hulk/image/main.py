#!/usr/bin/env python

def get_application():
    from google.appengine.ext.webapp import WSGIApplication
    from handlers import ImageUploadHandler
    return WSGIApplication(
        [
            (ImageUploadHandler.get_upload_url(), ImageUploadHandler),
        ],
        debug=True
    )
application = get_application()

def main():
    from google.appengine.ext.webapp import util
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
