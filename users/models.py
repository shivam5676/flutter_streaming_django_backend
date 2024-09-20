from django.db import models

from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    BooleanField,
    IntField,
    ListField,
)

# Create your models here


class Users(Document):
    name = StringField()
    email = StringField()
    password = StringField()
