"""
The ``agar.django.decorators`` module contains functions and decorators to help validate `django forms`_,
to be used to wrap :py:class:`agar.json.JsonRequestHandler` methods that accept input.
"""


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
    """
    A decorator that validates input matches with a `django form class`_.

    If the form is valid with the given request parameters, the decorator will add the bound form to the request under
    the ``form`` attribute and pass control on to the wrapped handler method.

    If the form doesn't validate, it will return a well-formed JSON response with a status code of ``400`` including an
    error dictionary describing the input errors.

    :param form_class: The `django form class`_ to use for input validation.
    """
    def decorator(request_method):
        def wrapped(self, *args, **kwargs):
            form = form_class(self.request.params)
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
