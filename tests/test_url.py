from env_setup import setup
setup()

from gaetestbed import WebTestCase
from unittest2 import TestCase

from agar.url import uri_for, url_for


class UriTest(WebTestCase, TestCase):
    def setUp(self):
        self.method = uri_for
        super(WebTestCase, self).setUp()

    def test_get_uri(self):
        uri = self.method('api-v1')
        self.assertEqual(uri, '/api/v1/model1')

    def test_get_invalid_uri_name(self):
        try:
            invalid_uri_name = 'invalid-uri-name'
            uri = uri_for(invalid_uri_name)
            self.fail("Got uri '%s' for invalid uri name '%s'" % (uri, invalid_uri_name))
        except Exception, e:
            self.assertEqual(e.message, "Route named '%s' is not defined." % invalid_uri_name)

class UrlTest(UriTest):
    def setUp(self):
        self.method = url_for
        super(WebTestCase, self).setUp()
