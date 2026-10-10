from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('create/', views.create_quiz_view, name='create_quiz'),
    path('my-quizzes/', views.my_quizzes_view, name='my_quizzes'),
    path('<int:quiz_id>/manage/', views.quiz_manage_view, name='quiz_manage'),
    path('<int:quiz_id>/edit/', views.quiz_edit_view, name='quiz_edit'),
    path('<int:quiz_id>/add-question/', views.add_question_view, name='add_question'),
    path('question/<int:question_id>/edit/', views.edit_question_view, name='edit_question'), 
    path('question/<int:question_id>/delete/', views.delete_question_view, name='delete_question'),
]