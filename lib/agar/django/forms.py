"""
The ``agar.django.forms`` module contains form classes to help using `django forms`_ with a `webapp2.Requesthandler`_.
"""

from django import forms


class HandlerForm(forms.Form):
    """
    A `django form class`_ that holds a reference to the current `webapp2.RequestHandler`_ handling the request.
    """
    def __init__(self, *args, **kwargs):
        self.handler = None
        super(HandlerForm, self).__init__(*args, **kwargs)


class StrictHandlerForm(HandlerForm):
    """
    A :py:class:`~agar.django.forms.HandlerForm` that validates all passed parameters are expected by the form.
    """
    def clean(self):
        field_keys = self.fields.keys()
        if self.handler is not None:
            param_keys = self.handler.request.params.keys()
            for key in param_keys:
                if key not in field_keys:
                    self._errors[key] = self.error_class(["Not a recognized parameter"])
        return self.cleaned_data
