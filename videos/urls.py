from django.contrib import admin
from django.urls import path
# from .views.upload import upload
# from .views.getVideo import getVideos
# from .views.deleteVideo import deleteVideo
# from .views.addAdsVideo import addAdsVideo
from .views.questionUploader import questionUploader
from .views.questionGenerator import generate_response
from .views.geminiQuestionHandler import generate_question_endpoint
urlpatterns = [
    path('uploadQuestions/',questionUploader),
    path('generateQuestions/',generate_response),
    path('questionHAndler/',generate_question_endpoint)
    # path('admin/', admin.site.urls),
    # path('upload/',upload),
    # path('getVideos/',getVideos),
    # path("deleteVideo/",deleteVideo),
    # path("adVideo/",addAdsVideo)
]