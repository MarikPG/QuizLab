from django.db import models
from django.conf import settings
from quizzes.models import Quiz, Question, Answer 


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    real_name = models.CharField(max_length=150, blank=True, null=True)
    score = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        name = self.real_name or (self.user.username if self.user else "Гість")
        return f"Спроба #{self.id} ({name}) — Квіз: {self.quiz.title}"


class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answers = models.ManyToManyField(Answer, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Відповідь на питання #{self.question.id} у спробі #{self.attempt.id}"