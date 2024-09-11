from django.urls import path
from .views.getSlider import getSliders
from .views.getMovieData import getMovieData
from django.contrib import admin

urlpatterns = [path("getSliders/", getSliders), path("getMovieData/", getMovieData)]
