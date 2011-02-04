from django.template import Node, TemplateSyntaxError

from google.appengine.ext.webapp import template


# Get the template Library
register = template.create_template_register()

class URLNode(Node):
    def __init__(self, route_name, args, kwargs, asvar):
        self.route_name = route_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(str(k), v.resolve(context))
                       for k, v in self.kwargs.items()])
        url = None
        try:
            from main import url_for
            url = url_for(self.route_name, *args, **kwargs)
        except Exception, e:
            if self.asvar is None:
                raise e
        url = url or ''
        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url

def url_for(parser, token):
    """
    Returns an absolute URL matching given the route with its parameters.

    This is a way to define links that aren't tied to a particular URL
    configuration::

        {% url_for route_name arg1,arg2,name1=value1 %}

    The first argument is a route name. Other arguments are comma-separated values
    that will be filled in place of positional and keyword arguments in the
    URL. All arguments for the URL should be present.

    For example if you have a route ``client`` taking client's id and
    the corresponding line in an application looks like this::

        ('/client/<id>', 'client')

    then in a template you can create a link for a certain client like this::

        {% url_for client id=client.id %}

    The URL will look like ``/client/123/``.
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (route name)" % bits[0])
    routename = bits[1]
    args = []
    kwargs = {}
    asvar = None

    if len(bits) > 2:
        bits = iter(bits[2:])
        for bit in bits:
            if bit == 'as':
                asvar = bits.next()
                break
            else:
                for arg in bit.split(","):
                    if '=' in arg:
                        k, v = arg.split('=', 1)
                        k = k.strip()
                        kwargs[k] = parser.compile_filter(v)
                    elif arg:
                        args.append(parser.compile_filter(arg))
    return URLNode(routename, args, kwargs, asvar)
url_for = register.tag(url_for)
