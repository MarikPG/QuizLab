from django.conf import settings
from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва квізу")
    description = models.TextField(blank=True, verbose_name="Опис")
    cover = models.ImageField(
        upload_to='quiz_covers/', 
        blank=True, 
        null=True, 
        verbose_name="Обкладинка"
    )
    code = models.CharField(
        max_length=10, 
        unique=True, 
        verbose_name="Код доступу"
    )
    time_limit_per_question = models.PositiveIntegerField(
        default=30, 
        verbose_name="Час на питання (сек)"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='quizzes',
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE, 
        related_name='questions', 
        verbose_name="Квіз"
    )
    text = models.TextField(verbose_name="Текст питання")
    media = models.FileField(
        upload_to='question_media/', 
        blank=True, 
        null=True, 
        verbose_name="Медіа (фото/відео)"
    )
    order = models.PositiveIntegerField(default=1, verbose_name="Порядок")

    def __str__(self):
        return f"{self.quiz.title} - Питання #{self.order}"


class Answer(models.Model):
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='answers', 
        verbose_name="Питання"
    )
    text = models.CharField(max_length=255, verbose_name="Текст відповіді")
    is_correct = models.BooleanField(default=False, verbose_name="Правильна відповідь")

    def __str__(self):
        return f"{self.text} ({'Правильна' if self.is_correct else 'Неправильна'})"