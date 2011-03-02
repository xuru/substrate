from env_setup import setup
setup()

# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
# 
# from google.appengine.dist import use_library
# use_library('django', '1.2')

from agar.env import on_production_server
from agar.json import JsonRequestHandler

from restler.serializers import ModelStrategy

from webapp2 import Route, RequestHandler, WSGIApplication

from models import Author, Book

AUTHOR_STRATEGY = ModelStrategy(Author, include_all_fields=True)


class AuthorHandler(RequestHandler):
    def get(self):
        self.response.out.write('Author Handler')

class IndexHandler(RequestHandler):
    def get(self):
        self.response.out.write('hello world')

class AuthorApiHandler(JsonRequestHandler):
    def get(self):
        authors = Author.all().fetch(100)
   
        self.json_response(authors, strategy=AUTHOR_STRATEGY) 
    

def get_application():
    return  WSGIApplication(
        [
            Route(r'/bookstore/api/author', AuthorApiHandler, 'author_api'),
            Route(r'/bookstore/author', AuthorHandler, 'author'),
            Route(r'/bookstore/', IndexHandler, 'index'),
        ],
        debug=not on_production_server
    )
application = get_application()

def main():
    from google.appengine.ext.webapp import util
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
