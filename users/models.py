from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Модель пользователя"""
    username = None
    telegram = models.CharField(max_length=50, unique=True, verbose_name='Телеграмм ник')
    token = models.CharField(max_length=50, verbose_name='Токен', null=True, blank=True)

    USERNAME_FIELD = 'telegram'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.telegram}'
