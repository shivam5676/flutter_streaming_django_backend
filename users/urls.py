from django.urls import path
from .views.createUser import createUser
from .views.signIn import signIn
from .views.usersGenreSelection import genreSelection
from .views.usersLAnguageSelection import usersLanguaseSelection
from .views.usersContentLanguageList import usersContentLanguageList
from .views.userGenreList import genreList

urlpatterns = [
    path("register/", createUser),
    path("signIn/", signIn),
    path("genreList/", genreList),
    path("genreSelector/", genreSelection),
    path("languageList/", usersContentLanguageList),
    path("languageSelector/", usersLanguaseSelection),
]