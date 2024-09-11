from pymongo import MongoClient
from django.conf import settings

# Create a MongoDB client
client = MongoClient(settings.MONGODB_URI)

# Access the default database
db = client.get_database('test')  # This uses the default database from the URI

# Define collections
sliders_collection = db.sliders
movies_collection = db.movies
shorts_collection = db.shorts
