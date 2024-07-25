from django.contrib import admin
from django.urls import path
from .views.upload import upload
from .views.getVideo import getVideos

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('upload/',upload),
    path('getVideos/',getVideos)
]