from google.appengine.ext import db


def new_iid():
    import uuid
    return uuid.uuid4().hex

class NamedModel(db.Model):
    """This base model has a classmethod for automatically asigning a
    new uuid for its key_name on creation of a new entity."""
    @classmethod
    def get_key_generator(cls, requested_key_name=None):
        if requested_key_name is not None:
            yield requested_key_name
        while 1:
          yield new_iid()

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
        requested_key_name = kwargs.pop('key_name', None)
        key_generator = cls.get_key_generator(requested_key_name=requested_key_name)
        first_key_name = key_generator.next()
        entity = db.run_in_transaction(txn, first_key_name)
        if requested_key_name is None:
            while entity is None:
                key_name = key_generator.next()
                entity = db.run_in_transaction(txn, key_name)
        return entity

class ModelException(Exception):
    pass
