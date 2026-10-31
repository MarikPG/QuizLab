from django.shortcuts import render, get_object_or_404
from quizzes.models import Quiz
from quiz_play.models import QuizAttempt  


def quiz_leaderboard_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    leaderboard = QuizAttempt.objects.filter(
        quiz=quiz, 
        is_completed=True
    ).order_by('-score', 'time_spent')[:20]

    context = {
        'quiz': quiz,
        'leaderboard': leaderboard
    }
    return render(request, 'analytics/leaderboard.html', context)