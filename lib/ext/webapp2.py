



def url_for(name, *args, **kwargs):
    # todo throw exception if no url found?
    from main import application as main_application
    owned_domain = kwargs.pop('owned_domain', True)
    request = kwargs.pop('request', None)
    _full = kwargs.get('_full', False)
    _netloc = kwargs.get('_netloc', None)
    if _netloc is None and _full and owned_domain and on_production_server:
        kwargs['_netloc'] = main_application.config.get_config('main', key='PRODUCTION_DOMAIN', default=[])
    if owned_domain:
        kwargs['_scheme'] = 'http'
    url = None
    APPLICATIONS = main_application.config.get_config('main', key='APPLICATIONS', default=[])
    for app_name in APPLICATIONS:
        app_module = __import__(app_name)
        try:
            application = app_module.application
            url = application.router.build(name, request, args, kwargs)
            if url is not None:
                break
        except KeyError:
            pass
    return url