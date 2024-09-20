from django.urls import path
from .views.getSlider import getSliders
from .views.getMovieData import getMovieData
from .views.getLayouts import getLayouts
from .views.getDataRelatedToLayouts import getDataRelatedToLayOuts
from django.contrib import admin

urlpatterns = [
    path("getSliders/", getSliders),
    path("getMovieData/", getMovieData),
    path("getLayouts/", getLayouts),
    path("getLayoutData/<movieID>", getDataRelatedToLayOuts),
]
