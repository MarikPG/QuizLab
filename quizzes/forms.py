from django import forms
from .models import Quiz, Question, Answer


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description', 'cover', 'code', 'time_limit_per_question', 'show_correct_immediately')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва квізу'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Опис'}),
            'cover': forms.FileInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наприклад: X7K9P2'}),
            'time_limit_per_question': forms.NumberInput(attrs={'class': 'form-control'}),
            'show_correct_immediately': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'media', 'order')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Текст питання'}),
            'media': forms.FileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text', 'is_correct')
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Варіант відповіді'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }