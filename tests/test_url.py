from env_setup import setup
setup()

from gaetestbed import WebTestCase
from unittest2 import TestCase

from agar.url import uri_for, url_for


class UriTest(WebTestCase, TestCase):
    def setUp(self):
        super(WebTestCase, self).setUp()

    def test_get_uri(self):
        uri = uri_for('api-v1')
        self.assertEqual(uri, '/api/v1/model1')

    def test_get_invalid_uri_name(self):
        try:
            invalid_uri_name = 'invalid-uri-name'
            uri = uri_for(invalid_uri_name)
            self.fail("Got uri '%s' for invalid uri name '%s'" % (uri, invalid_uri_name))
        except Exception, e:
            self.assertEqual(e.message, "Route named '%s' is not defined." % invalid_uri_name)

class UrlTest(WebTestCase, TestCase):
    def setUp(self):
        super(WebTestCase, self).setUp()

    def test_get_url(self):
        url = url_for('api-v1')
        self.assertEqual(url, '/api/v1/model1')

    def test_get_invalid_url_name(self):
        try:
            invalid_url_name = 'invalid-url-name'
            url = url_for(invalid_url_name)
            self.fail("Got uri '%s' for invalid url name '%s'" % (url, invalid_url_name))
        except Exception, e:
            self.assertEqual(e.message, "Route named '%s' is not defined." % invalid_url_name)
