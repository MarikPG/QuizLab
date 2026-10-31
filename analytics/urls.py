from django.urls import path
from . import views

urlpatterns = [
    path('quiz/<int:quiz_id>/leaderboard/', views.quiz_leaderboard_view, name='quiz_leaderboard'),
]