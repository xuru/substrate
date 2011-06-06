
import unittest
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import users

from restler import serializers
from tests.models import Model1, Model2


key = lambda obj: str(obj.key())
keys = lambda obj: [(str(o.key()) for o in obj)]
myprop = lambda obj: "this and %s" % obj.string

serialization = {
        Model1: (
            "string",
            {"myprop": myprop},
            {"key": key}
        ), 
}

class RestlerTest(unittest.TestCase):

    def setUp(self):
        for m in Model1.all(): m.delete()
        m = Model1()
        m.string = "this"
        m.put()
        m = Model1()
        m.string = "that"
        m.put()

    def test_serializers(self):
        ref = Model1()
        ref.put()
        m = Model1()
        m2 = Model2()
        m2.put()
        m.string = "string"
        m.bytestring = "\00\0x" 
        m.boolean = True 
        m.integer = 123
        m.float_ = 22.0 
        m.datetime = datetime.now() 
        m.date = datetime.now().date() 
        m.time = datetime.now().time() 
        m.list_ = [1,2,3]
        m.stringlist = ["one", "two", "three"] 
        m.reference = m2
        m.selfreference = ref
        m.blobreference = None # Todo
        m.user = users.get_current_user() 
        m.blob = "binary data" # Todo
        m.text = "text"
        m.category = "category"
        m.link = "http://www.yahoo.com" 
        m.email = "joe@yahoo.com" 
        m.geopt = "1.0, 2.0"
        m.im = "http://aim.com/ joe@yahoo.com" 
        m.phonenumber = "612-292-4339" 
        m.postaladdress = "234 Shady Oak Rd., Eden Prairie, MN, 55218" 
        m.rating = 23 
        m.put()
        #print serializers.to_json(m, serializers.ModelStrategy(Model1) - ("selfreference", "blobreference"))

'''
    def test_simple(self):
        self.assertEqual(serializers.to_json(Model1().all(), serialization), 
               """[{"string": "this", "key": "agZyZXN0bGVyDgsSB015TW9kZWwYtwEM", "myprop": "this and this"}, {"string": "that", "key": "agZyZXN0bGVyDgsSB015TW9kZWwYuAEM", "myprop": "this and that"}]""")

    def test_simple_properties(self):
        self.assertTrue(True)
'''


