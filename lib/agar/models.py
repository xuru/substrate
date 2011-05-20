from google.appengine.ext import db


class NamedModel(db.Model):
    """Base model to create an Entity with a key name.

    This base model has a classmethod for automatically asigning a
    new uuid for its key_name on creation of a new entity.

    """

    @property
    def key_name(self):
        """ Return the entity.key().name() unicode value if available, otherwise None.
            
            Use NamedModel.key_name_str() for string value.
            
        """
        if self.key():
            return self.key().name()
        return None

    @property
    def key_name_str(self):
        """ Return the entity.key().name() string value if available, otherwise None.
            
            Use NamedModel.key_name_str() for unicode value.
        """
        if self.key_name:
            return str(self.key_name)
        return None

    @classmethod
    def generate_key_name(cls):
        import uuid
        return uuid.uuid4().hex

    @classmethod
    def create_new_entity(cls, **kwargs):
        """ Creates a new entity unless the key_name parameter is found.

        Keyword arguments:
            key_name -- Used for the entity key name, otherwise will be generated.

        Creates and persists an Entity by generating and setting a key_name.
        If a key_name is provided as a named argument,
        Entity.get_by_key_name(key_name) will be invoked.
        If found, the entiry will be returned otherwise a new entity will be created.

        person = Person.create_new_entity()

        """
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
