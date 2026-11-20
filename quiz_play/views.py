from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Q
from django.utils import timezone
from django.contrib import messages
from quizzes.models import Quiz, Question, Answer
from .models import QuizAttempt, UserAnswer

def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if not quiz.can_access(request):
        messages.error(request, 'Це приватний квіз. Введіть його код на головній сторінці.')
        return redirect('home')
    
    if request.method == 'POST':
        real_name = request.POST.get('real_name', '').strip()
        
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            user=request.user if request.user.is_authenticated else None,
            real_name=real_name or (request.user.username if request.user.is_authenticated else 'Гість')
        )
        
        request.session['active_attempt_id'] = attempt.id
        request.session['current_question_index'] = 0
        
        return redirect('play_quiz', quiz_id=quiz.id)
        
    return render(request, 'quiz_play/start.html', {'quiz': quiz})


def play_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if not quiz.can_access(request):
        messages.error(request, 'Це приватний квіз. Введіть його код на головній сторінці.')
        return redirect('home')
    attempt_id = request.session.get('active_attempt_id')
    
    if not attempt_id:
        return redirect('start_quiz', quiz_id=quiz.id)
        
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, quiz=quiz)
    questions = list(quiz.questions.all().order_by('order'))
    current_index = request.session.get('current_question_index', 0)
    
    if current_index >= len(questions):
        attempt.is_completed = True
        attempt.finished_at = timezone.now()
        
        if attempt.started_at:
            delta = attempt.finished_at - attempt.started_at
            attempt.time_spent = int(delta.total_seconds())
            
        attempt.save()
        return redirect('quiz_results', attempt_id=attempt.id)
        
    current_question = questions[current_index]
    
    if request.method == 'POST':
        if request.POST.get('question_id') and request.POST.get('question_id') != str(current_question.id):
            return redirect('play_quiz', quiz_id=quiz.id)

        selected_answer_ids = request.POST.getlist('answers')
        selected_answers = Answer.objects.filter(id__in=selected_answer_ids, question=current_question)
        
        correct_answers = set(current_question.answers.filter(is_correct=True).values_list('id', flat=True))
        user_answers = set(selected_answers.values_list('id', flat=True))
        is_correct = (correct_answers == user_answers)
        
        user_answer, created = UserAnswer.objects.get_or_create(
            attempt=attempt,
            question=current_question,
            defaults={'is_correct': is_correct}
        )
        if not created:
            request.session['current_question_index'] = current_index + 1
            return redirect('play_quiz', quiz_id=quiz.id)
        user_answer.selected_answers.set(selected_answers)
        
        if is_correct:
            attempt.score += 1
            attempt.save()
            
        request.session['current_question_index'] = current_index + 1
        return redirect('play_quiz', quiz_id=quiz.id)
        
    context = {
        'quiz': quiz,
        'question': current_question,
        'current_number': current_index + 1,
        'total_questions': len(questions),
        'is_multiple': current_question.answers.filter(is_correct=True).count() > 1,
        'time_limit': quiz.time_limit_per_question,
        'time_limit_label': '%02d:%02d' % divmod(quiz.time_limit_per_question, 60),
    }
    return render(request, 'quiz_play/play.html', context)


def quiz_results(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    if not attempt.quiz.can_access(request):
        messages.error(request, 'Це приватний квіз. Введіть його код на головній сторінці.')
        return redirect('home')
    done = QuizAttempt.objects.filter(quiz=attempt.quiz, is_completed=True)
    total = attempt.quiz.questions.count()
    better = done.filter(Q(score__gt=attempt.score) | Q(score=attempt.score, time_spent__lt=attempt.time_spent)).count()

    return render(request, 'quiz_play/results.html', {
        'attempt': attempt,
        'total': total,
        'percent': round(attempt.score * 100 / total) if total else 0,
        'place': better + 1,
        'players': done.count(),
        'avg_score': round(done.aggregate(a=Avg('score'))['a'] or 0, 1),
        'answers': attempt.user_answers.order_by('id'),
        'leaderboard': done.order_by('-score', 'time_spent')[:10],
    })