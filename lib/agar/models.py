from google.appengine.ext import db
from google.appengine.ext.db import BadKeyError


class NamedModel(db.Model):
    """
A base (or mix-in) model to create an entity with a ``key_name`` (either passed in or generated automatically).

This base model has a classmethod for automatically assigning a new uuid for its ``key_name`` on creation of a new entity.
    """
    @property
    def key_name(self):
        """
        Return the ``entity.key().name()`` unicode value if available, otherwise ``None``.
            
        Use ``key_name_str`` for string (as opposed to unicode) value.
        """
        return self.key().name()

    @property
    def key_name_str(self):
        """
        Return the ``entity.key().name()`` as a string (as opposed to a unicode) value if available, otherwise ``None``.

        Use ``key_name`` for unicode value.
        """
        if self.key_name:
            return str(self.key_name)
        return None

    @classmethod
    def generate_key_name(cls):
        """
        Returns a (hopefully) unique string to be used as an identifier. The default implementation uses a ``uuid4`` hex value.
        """
        import uuid
        return uuid.uuid4().hex

    @classmethod
    def create_new_entity(cls, **kwargs):
        """
        Creates a new entity unless the ``key_name`` parameter is already in use for the given entity kind, in which case it
        raises a ``google.appengine.ext.db.BadKeyError`` exception.

        Keyword arguments:
            ``key_name`` -- Used for the entity key name, otherwise will be generated.

            ``parent`` -- Optional parent key. If not supplied, defaults to ``None``.

        Creates and persists an entity by (optionally) generating and setting a ``key_name``.
        A ``key_name`` will be generated or may be provided as a keyword arg.  If a generated ``key_name`` is already in use,
        a new one will be generated.  If, after the 3rd attempt the ``key_name`` is still not unique, a ``google.appengine.ext.db.BadKeyError``
        exception will be raised.  This exception will also be raised if a passed in ``key_name`` is not unique.

        Examples::

            person = Person.create_new_entity()

            person_with_keyname = Person.create_new_entity(key_name='bob')
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
                raise BadKeyError("key_name '%s' is already in use" % key_name)
        
        # Function body
        entity = None
        tries = 0
        requested_key_name = kwargs.pop('key_name', None)
        if requested_key_name:
            entity = db.run_in_transaction(txn, requested_key_name)
        else:
            while entity is None:
                try:
                    entity = db.run_in_transaction(txn, cls.generate_key_name())
                except BadKeyError:
                    tries += 1
                    if tries >= 3:
                        raise
        return entity

class ModelException(Exception):
    pass
