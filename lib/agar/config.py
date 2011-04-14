from google.appengine.api import lib_config

class Config(object):
    _namespace = 'agar'

    def __init__(self, **kwargs):
        self.defaults = {}
        for setting in self.__class__.__dict__.keys():
            if not setting.startswith('_'):
                self.defaults[setting] = self.__class__.__dict__[setting]
        for key in kwargs.keys():
            if key in self.defaults.keys():
                self.defaults[key] = kwargs[key]
            else:
                raise AttributeError('Invalid config key: %s' % key)

    @classmethod
    def get_config(cls, **kwargs):
        return lib_config.register(cls._namespace, cls(**kwargs).defaults)
