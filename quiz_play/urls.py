from django.urls import path
from . import views

urlpatterns = [
    path('<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('<int:quiz_id>/play/', views.play_quiz, name='play_quiz'),
    path('results/<int:attempt_id>/', views.quiz_results, name='quiz_results'),
]