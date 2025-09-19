from django.urls import path
from .views import getQuestions,insertQuestion,dataEntry

urlpatterns = [
    path('questions/<str:category>/', getQuestions, name="get_questions"),
    path('',dataEntry,name='data-entry'),
    path('insert-data/',insertQuestion,name='insert-data')
]
