# JSON Handler Base Class
from google.appengine.api.mail_errors import BadRequestError
from api import string_to_int

class JsonRequestHandler(RequestHandler):
    def json_response(self, model_or_query, strategy=None, status_code=200, status_text='OK', context=None):
        if not context:
            context = {}
        context['request'] = self.request
        data = dict()
        data['status_code'] = status_code
        data['status_text'] = status_text
        data['data'] = model_or_query
        return restler_json_response(self.response, data, strategy=strategy, status_code=status_code, context=context)

    def handle_exception(self, exception, debug_mode):
        status_text = exception.message
        if isinstance(exception, HTTPException):
            code = exception.code
        elif isinstance(exception, ModelException):
            code = 400
            status_text = "%s: %s" % (BAD_REQUEST, status_text)
        else:
            code = 500
            status_text = "%s: %s" % (INTERNAL_SERVER_ERROR, status_text)
            if debug_mode:
                logging.error("INTERNAL_SERVER_ERROR %s: %s" % (code, status_text))
        if code == 401:
            status_text = UNAUTHORIZED
        if code == 404:
            status_text = NOT_FOUND
        if code == 405:
            status_text = METHOD_NOT_ALLOWED
        return self.json_response({}, status_code=code, status_text=status_text)

# A RequestHandler class to help with 'page_size' and 'page_key' parsing and logic
class MultiPageHandler(JsonRequestHandler):
    @property
    def page_size(self):
        DEFAULT_PAGE_SIZE = application.config.get_config('api', key='DEFAULT_PAGE_SIZE', default=10)
        MAX_PAGE_SIZE = application.config.get_config('api', key='MAX_PAGE_SIZE', default=100)
        page_size = string_to_int(self.request.get('page_size', str(DEFAULT_PAGE_SIZE)))
        page_size = min(max(page_size, 1), MAX_PAGE_SIZE)
        return page_size

    def fetch_page(self, query):
        cursor = self.request.get('page_key', None)
        if cursor is not None:
            try:
                query = query.with_cursor(cursor)
            except BadRequestError:
                self.abort(400, "The 'page_key' has expired: %s" % cursor)
        results = query.fetch(self.page_size)
        next_page_key = None
        if len(results) == self.page_size:
            next_page_key = query.cursor()
        return results, next_page_key