


# Authorization
def authorize_api_key(request):
    from main import on_production_server
    scheme, netloc, path, query, fragment = urlparse.urlsplit(request.url)
    # Only allow HTTPS on PRODuction
    if on_production_server and scheme and scheme.lower() != 'https':
        return False
    api_key = request.get('api_key', default_value=None)
    VALID_API_KEYS = application.config.get_config('api', key='VALID_API_KEYS', default=None)
    return api_key in VALID_API_KEYS

def api_key_required(method):
    def authorize_api_key(handler, *args, **kwargs):
        if authorize(handler.request):
            method(handler, *args, **kwargs)
        else:
            handler.abort(401)
    return authorized_method
