
import unittest
from google.appengine.ext import db

from restler import serializers
from models import MyModel

key = lambda cls, obj: str(obj.key())
myprop = lambda cls, obj: "this and %s" % obj.prop1

serialization = {
        MyModel: (
            "prop1", 
            ("myprop", myprop), 
            ("key", key)
        ), 
}
fields = ("prop1", 
         ("myprop", myprop), 
         ("key", key))

class RestlerTest(unittest.TestCase):

    def setUp(self):
        for m in MyModel.all(): m.delete()
        m = MyModel()
        m.prop1 = "this"
        m.put()
        m = MyModel()
        m.prop1 = "that"
        m.put()

    def test_simple(self):
        self.assertEqual(serializers.to_json(MyModel().all(), serialization), 
               """[{"prop1": "this", "key": "agZyZXN0bGVyDgsSB015TW9kZWwYtwEM", "myprop": "this and this"}, {"prop1": "that", "key": "agZyZXN0bGVyDgsSB015TW9kZWwYuAEM", "myprop": "this and that"}]""")

    def test_simple_properties(self):
        self.assertTrue(True)
