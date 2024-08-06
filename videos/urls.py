from django.contrib import admin
from django.urls import path
from .views.upload import upload
from .views.getVideo import getVideos
from .views.deleteVideo import deleteVideo
from .views.addAdsVideo import addAdsVideo
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('upload/',upload),
    path('getVideos/',getVideos),
    path("deleteVideo/",deleteVideo),
    path("adVideo/",addAdsVideo)
]