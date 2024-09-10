from django.urls import path
from .views.getSlider import getSlider
from django.contrib import admin

urlpatterns = [
    path("getSliders/",getSlider),
    
]
