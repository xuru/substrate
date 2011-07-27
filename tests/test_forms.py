import urllib

from gaetestbed import WebTestCase, DataStoreTestCase

from unittest2 import TestCase

from agar.url import uri_for

from api import application


class FormTest(WebTestCase, DataStoreTestCase, TestCase):
    APPLICATION = application

    def setUp(self):
        self.uri = uri_for('api-v1')
        super(FormTest, self).setUp()

    def test_get(self):
        response = self.get(self.uri)
        self.assertOK(response)
        data = response.json['data']
        self.assertEqual(len(data), 2)
        models = data[0]
        self.assertEqual(len(models), 10)
        cursor = data[1]
        self.assertIsNotNone(cursor)

    def test_get_page_size(self):
        params = urllib.urlencode({'page_size': 5})
        response = self.get("%s?%s" % (self.uri, params))
        self.assertOK(response)
        data = response.json['data']
        self.assertEqual(len(data), 2)
        models = data[0]
        self.assertEqual(len(models), 5)
        cursor = data[1]
        self.assertIsNotNone(cursor)
