from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from .models import Quiz, Question, Answer
from .forms import QuizForm, QuestionForm, AnswerForm


def home_view(request):
    search_query = request.GET.get('q', '')
    
    if search_query:
        quizzes = Quiz.objects.filter(is_public=True, title__icontains=search_query).order_by('-created_at')
    else:
        quizzes = Quiz.objects.filter(is_public=True).order_by('-created_at')

    if request.method == 'POST':
        code = request.POST.get('quiz_code', '').strip()
        if code:
            quiz = Quiz.objects.filter(code=code).first()
            if quiz:
                return redirect('quiz_manage', quiz_id=quiz.id)
            else:
                messages.error(request, 'Квіз із таким кодом не знайдено.')

    return render(request, 'quizzes/home.html', {
        'quizzes': quizzes,
        'search_query': search_query
    })


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

@login_required
def quiz_edit_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if quiz.author != request.user and not request.user.is_superuser and getattr(request.user, 'role', '') != 'admin':
        messages.error(request, 'У вас немає прав для редагування цього квізу.')
        return redirect('home')

    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Налаштування квізу успішно оновлено!')
            return redirect('quiz_manage', quiz_id=quiz.id)
    else:
        form = QuizForm(instance=quiz)

    return render(request, 'quizzes/quiz_edit.html', {'form': form, 'quiz': quiz})


@login_required
def delete_question_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz = question.quiz

    if quiz.author != request.user and not request.user.is_superuser and getattr(request.user, 'role', '') != 'admin':
        messages.error(request, 'Доступ заборонено.')
        return redirect('home')

    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Питання успішно видалено.')

    return redirect('quiz_manage', quiz_id=quiz.id)

@login_required
def edit_question_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz = question.quiz

    if quiz.author != request.user and not request.user.is_superuser and getattr(request.user, 'role', '') != 'admin':
        messages.error(request, 'Доступ заборонено.')
        return redirect('home')

    AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=0, can_delete=True)

    if request.method == 'POST':
        q_form = QuestionForm(request.POST, request.FILES, instance=question)
        formset = AnswerFormSet(request.POST, queryset=question.answers.all())

        if q_form.is_valid() and formset.is_valid():
            q_form.save()
            
            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()

            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

            messages.success(request, 'Питання успішно оновлено!')
            return redirect('quiz_manage', quiz_id=quiz.id)
    else:
        q_form = QuestionForm(instance=question)
        formset = AnswerFormSet(queryset=question.answers.all())

    return render(request, 'quizzes/edit_question.html', {
        'quiz': quiz,
        'question': question,
        'q_form': q_form,
        'formset': formset
    })