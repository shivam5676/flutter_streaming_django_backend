from django.urls import path
from .views.createUser import createUser
from .views.signIn import signIn
from .views.usersGenreSelection import genreSelection

urlpatterns = [
    path("register/", createUser),
    path("signIn/", signIn),
    path("genreSelector/",genreSelection),
]
