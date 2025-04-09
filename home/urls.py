from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = "home"),
    path('add_question', add_question, name = "add_question"),
    path('answer_question', answer_question, name = "answer_question"),
    path('like_answer', like_answer, name = "like_answer")
]