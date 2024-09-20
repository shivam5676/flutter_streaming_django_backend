# from django.db import models
from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    BooleanField,
    IntField,
    ListField,
)


# Create your models here.



class Slider(Document):
    schemaName = StringField()
    type = StringField()
    linkedMovie = ReferenceField('Movies')


class Layout(Document):
    name = StringField()
    Description = StringField()
    linkedMovies = ListField(ReferenceField('Movies'))
    
class Movies(Document):  # Fixed 'document' to 'Document'
    name = StringField()
    genre = StringField()
    layout = StringField()
    freeVideos = IntField(required=True)
    visible = BooleanField(required=True)  # Missing parentheses fixed
    fileLocation = StringField()
    shorts = ListField(ReferenceField('Shorts'))  # Reference to Shorts
    layouts = ListField(ReferenceField('Layout'))  # Reference to Layout
    # __v = IntField(required=False)

class Shorts(Document):
    name = StringField()
    fileLocation = StringField()
    genre = StringField()
    visible = BooleanField(required=True)
    Movies = ReferenceField('Movies')
