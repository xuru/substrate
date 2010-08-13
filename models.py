
from google.appengine.ext import db

class MyModel(db.Model):

    __serialize__ = ("prop1", "prop2")

    prop1 = db.StringProperty()



class RestModel(MyModel):
    pass
    #fields = (MyModel.prop1)



