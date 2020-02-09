from mongoengine import Document
from mongoengine.fields import StringField


class User(Document):
    meta = {'collection': 'user'}
    name = StringField(required=True)
    image = StringField(required=True)
    time = StringField(required=True)
