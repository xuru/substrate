
from google.appengine.ext import db

class MyModel(db.Model):

    __serialize__ = ("prop1", "myprop")

    prop1 = db.StringProperty()

    @classmethod
    def myprop(cls, obj):
        return "this %s" %obj.prop1


class RestModel(MyModel):
    pass
    #fields = (MyModel.prop1)



