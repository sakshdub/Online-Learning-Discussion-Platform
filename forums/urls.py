from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:course_id>/', views.question_list, name='question_list'),
    path('course/<int:course_id>/add/', views.add_question, name='add_question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    
    # THIS IS THE MISSING LINE - Add it for the vote feature
    path('vote_answer/<int:answer_id>/', views.vote_answer, name='vote_answer'),
]