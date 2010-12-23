import unittest


class ConfigTest(unittest.TestCase):
    def test_config(self):
        from google.appengine.api import lib_config
        config = lib_config.register('hulk_url', {'APPLICATIONS': []})
        self.assertEqual(config.APPLICATIONS, ['main', 'api'])
