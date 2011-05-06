def create_error_dict(error_list):
    from django.forms.util import ErrorList
    text_errors = {}
    for key, value in error_list.items():
        if isinstance(value, ErrorList):
            text_errors[key] = value.as_text()
        else:
            text_errors[key] = value
    return text_errors

def validate_service(form_class):
    def decorator(request_method):
        def wrapped(self, *args, **kwargs):
            form = form_class(self.request.params, handler=self)
            if form.is_valid():
                self.request.form = form
                request_method(self, *args, **kwargs)
                return
            else:
                error_dict = create_error_dict(form.errors)
                status_text = "BAD_REQUEST"
                self.json_response({}, status_code=400, status_text=status_text, errors=error_dict)
                return
        return wrapped
    return decorator
