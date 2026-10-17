from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from quizzes.models import Quiz, Question, Answer
from .models import QuizAttempt, UserAnswer

def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
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
    attempt_id = request.session.get('active_attempt_id')
    
    if not attempt_id:
        return redirect('start_quiz', quiz_id=quiz.id)
        
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    questions = list(quiz.questions.all().order_by('id'))
    current_index = request.session.get('current_question_index', 0)
    
    if current_index >= len(questions):
        attempt.is_completed = True
        attempt.finished_at = timezone.now()
        attempt.save()
        return redirect('quiz_results', attempt_id=attempt.id)
        
    current_question = questions[current_index]
    
    if request.method == 'POST':
        selected_answer_ids = request.POST.getlist('answers')
        selected_answers = Answer.objects.filter(id__in=selected_answer_ids, question=current_question)
        
        correct_answers = set(current_question.answers.filter(is_correct=True).values_list('id', flat=True))
        user_answers = set(selected_answers.values_list('id', flat=True))
        is_correct = (correct_answers == user_answers)
        
        user_answer = UserAnswer.objects.create(
            attempt=attempt,
            question=current_question,
            is_correct=is_correct
        )
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
        'is_multiple': current_question.answers.filter(is_correct=True).count() > 1
    }
    return render(request, 'quiz_play/play.html', context)


def quiz_results(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    return render(request, 'quiz_play/results.html', {'attempt': attempt})