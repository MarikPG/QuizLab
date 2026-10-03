from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from .models import Quiz, Question, Answer
from .forms import QuizForm, QuestionForm, AnswerForm


def home_view(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quizzes/home.html', {'quizzes': quizzes})


@login_required
def create_quiz_view(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = request.user
            quiz.save()
            messages.success(request, f'Квіз "{quiz.title}" успішно створено! Тепер додайте питання.')
            return redirect('quiz_manage', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'quizzes/create_quiz.html', {'form': form})


@login_required
def quiz_manage_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if quiz.author != request.user and not request.user.is_superuser and getattr(request.user, 'role', '') != 'admin':
        messages.error(request, 'У вас немає прав для редагування цього квізу.')
        return redirect('home')

    questions = quiz.questions.all().order_by('order')
    return render(request, 'quizzes/quiz_manage.html', {'quiz': quiz, 'questions': questions})


@login_required
def add_question_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if quiz.author != request.user and not request.user.is_superuser and getattr(request.user, 'role', '') != 'admin':
        messages.error(request, 'Доступ заборонено.')
        return redirect('home')

    AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=4, can_delete=False)

    if request.method == 'POST':
        q_form = QuestionForm(request.POST, request.FILES)
        formset = AnswerFormSet(request.POST, queryset=Answer.objects.none())

        if q_form.is_valid() and formset.is_valid():
            question = q_form.save(commit=False)
            question.quiz = quiz
            question.save()

            for answer_form in formset:
                if answer_form.cleaned_data and answer_form.cleaned_data.get('text'):
                    answer = answer_form.save(commit=False)
                    answer.question = question
                    answer.save()

            messages.success(request, 'Питання та варіанти відповідей додано!')
            return redirect('quiz_manage', quiz_id=quiz.id)
    else:
        q_form = QuestionForm()
        formset = AnswerFormSet(queryset=Answer.objects.none())

    return render(request, 'quizzes/add_question.html', {
        'quiz': quiz,
        'q_form': q_form,
        'formset': formset
    })

@login_required
def my_quizzes_view(request):
    quizzes = Quiz.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'quizzes/my_quizzes.html', {'quizzes': quizzes})