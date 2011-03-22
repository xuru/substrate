


def create_error_dict(error_list):
    from django.forms.util import ErrorList

    text_errors = {}
    for key, value in error_list.items():
        if isinstance(value, ErrorList):
            text_errors[key] = value.as_text()
        else:
            text_errors[key] = value
    return text_errors


def validate_service(Form):
    def decorator(request_method):
        def wrapped(self, *args, **kwargs):
            form = Form(self.request.params)
            if form.is_valid():
                self.request.form = form
                request_method(self, *args, **kwargs)
                return
            else:
                error_dict = create_error_dict(form.errors)
                self.json_response({'errors':error_dict}, status_code=400)
                return
                
        return wrapped
    return decorator

