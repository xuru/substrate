from env_setup import setup
setup()

from gaetestbed import DataStoreTestCase
from google.appengine.ext import db
from unittest2 import TestCase

from agar.models import NamedModel

class NamedModelTests(DataStoreTestCase, TestCase):

    def setUp(self):
        super(DataStoreTestCase, self).setUp()
        self.clear_datastore()

    def test_create_new_entity(self):
        class TestModel(NamedModel):
            string = db.StringProperty(required=True)
        
        model = TestModel.create_new_entity(string='test entity')
        self.assertIsNone(model.key().id())
        self.assertIsNotNone(model.key().name())
    
    def test_create_with_key_name(self):
        class TestModel(NamedModel):
            string = db.StringProperty(required=True)
        
        model = TestModel.create_new_entity(string='test entity', key_name='test_key')
        self.assertIsNone(model.key().id())
        self.assertEquals('test_key', model.key().name())
    
    def test_create_with_duplicate_key_name(self):
        class TestModel(NamedModel):
            string = db.StringProperty(required=True)
        
        model1 = TestModel.create_new_entity(string='test entity1', key_name='test_key')
        model2 = TestModel.create_new_entity(string='test entity2', key_name='test_key')
        self.assertIsNone(model2)

    def test_create_with_key_name_and_parent(self):
        class ParentModel(NamedModel):
            string = db.StringProperty(required=True)

        class TestModel(NamedModel):
            string = db.StringProperty(required=True)
        
        parent = ParentModel.create_new_entity(string='parent')
        model = TestModel.create_new_entity(
            string='test entity', key_name='test_key', parent=parent.key())
        self.assertIsNone(model.key().id())
        self.assertEquals('test_key', model.key().name())
        self.assertEquals(parent.key(), model.parent_key())

    def test_key_name_property(self):
        class TestModel(NamedModel):
            string = db.StringProperty(required=True)
        
        model = TestModel.create_new_entity(string='test entity')
        self.assertIsInstance(model.key_name, unicode)

    def test_key_name_property_is_none(self):
        class TestModel(NamedModel):
            string = db.StringProperty(required=True)
        
        model = TestModel(string='test entity')
        model.put()
        self.assertIsNone(model.key_name)

    def test_key_name_str_property(self):
        class TestModel(NamedModel):
            string = db.StringProperty(required=True)
        
        model = TestModel.create_new_entity(string='test entity')
        self.assertIsInstance(model.key_name_str, str)

    def test_key_name_str_property_is_none(self):
        class TestModel(NamedModel):
            string = db.StringProperty(required=True)
        
        model = TestModel(string='test entity')
        model.put()
        self.assertIsNone(model.key_name_str)
