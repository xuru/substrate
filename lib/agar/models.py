from google.appengine.ext import db


class NamedModel(db.Model):
    """This base model has a classmethod for automatically asigning a
    new uuid for its key_name on creation of a new entity."""
    @property
    def key_name(self):
        if self.key():
            return self.key().name()
        return None

    @property
    def key_name_str(self):
        if self.key_name:
            return str(self.key_name)
        return None

    @classmethod
    def generate_key_name(cls):
        import uuid
        return uuid.uuid4().hex

    @classmethod
    def create_new_entity(cls, **kwargs):
        # Inline transaction function
        def txn(key_name):
            if kwargs.has_key('parent'):
                entity = cls.get_by_key_name(key_name, parent=kwargs['parent'])
            else:
                entity = cls.get_by_key_name(key_name)
            if entity is None:
                entity = cls(key_name=key_name, **kwargs)
                entity.put()
                return entity
            else:
                return None
        # Function body
        entity = None
        requested_key_name = kwargs.pop('key_name', None)
        if requested_key_name:
            entity = db.run_in_transaction(txn, requested_key_name)
        else:
            while entity is None:
                entity = db.run_in_transaction(txn, cls.generate_key_name())
        return entity

class ModelException(Exception):
    pass
