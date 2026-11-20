from django.db.models import Avg, Count, Max
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from quizzes.models import Quiz
from quiz_play.models import QuizAttempt


def quiz_leaderboard_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if not quiz.can_access(request):
        messages.error(request, 'Це приватний квіз. Введіть його код на головній сторінці.')
        return redirect('home')
    done = QuizAttempt.objects.filter(quiz=quiz, is_completed=True)
    return render(request, 'analytics/leaderboard.html', {
        'quiz': quiz,
        'total': quiz.questions.count(),
        'stats': done.aggregate(players=Count('id'), best=Max('score'), avg=Avg('score')),
        'leaderboard': done.order_by('-score', 'time_spent')[:20],
    })