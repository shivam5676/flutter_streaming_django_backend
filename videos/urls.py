from django.contrib import admin
from django.urls import path


from .views.questionUploader import questionUploader
from .views.questionGenerator import generate_response
from .views.geminiQuestionHandler import generate_question_endpoint

urlpatterns = [
    path("uploadQuestions/", questionUploader),
    path("generateQuestions/", generate_response),
    path("questionHAndler/", generate_question_endpoint),
]
