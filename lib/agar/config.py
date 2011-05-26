from google.appengine.api import lib_config

class Config(object):
    """
    Configurable constants base class for use with the excellent
    `google.appengine.api.lib_config <http://code.google.com/p/googleappengine/source/browse/trunk/python/google/appengine/api/lib_config.py>`_
    configuration library. A short write-up of this library can be found `here <https://profiles.google.com/u/0/thomasbohmbach/posts/FaxYvaSYuMa>`_.

    To use this class, create a subclass that redefines :py:attr:`~agar.config.Config._namespace` to the appengine_config namespace you'd like the
    configs to appear under.  Then, simply create class-level properties/functions/default values for each constant.

    When instantiating an instance of this class, you can override the default values for that instance by passing
    in new defaults via the constructor.  Of course, if there is an entry in ``appengine_config.py`` for your constant, that
    value will supersede any defined in the class or passed in via the constructor.

    Example::

        class SampleConfig(Config):
            _namespace = 'test'

            STRING_CONFIG = 'defaultstring'

    ::

        >>> config = SampleConfig.get_config()
        >>> custom_config = SampleConfig.get_config(STRING_CONFIG='customstring')

    Assuming there is no override for ``test_STRING_CONFIG`` in ``appengine_config.py``::

        >>> config.STRING_CONFIG == 'defaultstring'
        True
        >>> custom_config.STRING_CONFIG == 'customstring'
        True

    Assuming ``appengine_config.py`` contains the following line::

        test_STRING_CONFIG = 'settingstring'

    Then::

        >>> config.STRING_CONFIG == custom_config.STRING_CONFIG == 'settingstring'
        True
    """

    #: The appengine_config namespace that the configs should appear under. Override in subclasses. The default is ``agar``.
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
        """
        Registers and returns the lib_config ``ConfigHandle`` for the class. Keyword arguments will override default
        values defined in the :py:class:`~agar.config.Config` subclass (but, of course, will still defer to values in
        the ``appengine_config.py`` file).
        """
        return lib_config.register(cls._namespace, cls(**kwargs).defaults)
