from django.urls import path
from .views import getQuestions

urlpatterns = [
    path('questions/', getQuestions, name="get_questions"),
]