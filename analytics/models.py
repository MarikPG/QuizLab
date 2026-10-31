from django.conf import settings
from django.db import models
from quizzes.models import Quiz


class QuizSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='quiz_sessions',
        verbose_name="Користувач",
        null=True, blank=True 
    )
    real_name = models.CharField(max_length=100, blank=True, verbose_name="Ім'я гравця") 
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE, 
        related_name='sessions',
        verbose_name="Квіз"
    )
    score = models.PositiveIntegerField(default=0, verbose_name="Набрані бали")
    total_questions = models.PositiveIntegerField(default=0, verbose_name="Всього питань")
    time_spent = models.PositiveIntegerField(default=0, verbose_name="Час проходження (сек)")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата проходження")

    def __str__(self):
        name = self.real_name or (self.user.username if self.user else "Гість")
        return f"{name} - {self.quiz.title}: {self.score} балів ({self.time_spent}с)"