from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Користувач'),
        ('admin', 'Адміністратор'),
    )

    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='user', 
        verbose_name="Роль"
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True, 
        verbose_name="Аватар"
    )
    bio = models.TextField(
        max_length=500, 
        blank=True, 
        verbose_name="Про себе"
    )

    def is_admin_role(self):
        return self.role == 'admin' or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"