from django.urls import path
from .views.getSlider import getSliders
from .views.getMovieData import getMovieData
from .views.getLayouts import getLayouts
from .views.getDataRelatedToLayouts import getDataRelatedToLayOuts
from django.contrib import admin
from .views.refreshTheVideoURL import refreshTheVideoURL
from .views.purchasePremiumVideo import purchasePremiumVideo
urlpatterns = [
    path("getSliders/", getSliders),
    path("getMovieData/", getMovieData),
    path("getLayouts/", getLayouts),
    path("getLayoutData/<layoutID>", getDataRelatedToLayOuts),
    path("purchaseVideo/",purchasePremiumVideo),
    path("rfVid",refreshTheVideoURL)
    
]
