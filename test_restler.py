
import unittest
from google.appengine.ext import db

from restler import serializers
from models import MyModel
from ae_test_data.builder import build
db.Model.build = classmethod(build)

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
        # m = MyModel()
        # m.prop1 = "this"
        # m.put()
        # m = MyModel()
        # m.prop1 = "that"
        # m.put()
        self.this = MyModel.build(prop1='this')
        self.that = MyModel.build(prop1='that')

    def test_simple(self):
        self.assertEqual(2, len(MyModel.all().fetch(10)))
        self.assertEqual(serializers.to_json(MyModel.all(), serialization), 
               """[{"prop1": "this", "key": "%s", "myprop": "this and this"}, {"prop1": "that", "key": "%s", "myprop": "this and that"}]"""% (self.this.key(), self.that.key()))

    def test_simple_properties(self):
        self.assertTrue(True)
