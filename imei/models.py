from django.db import models

class TokenTG(models.Model):
    """Модель токена."""
    name = models.CharField(max_length=50, verbose_name='Токен', unique=True)

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'

    def __str__(self):
        return f'{self.name}'
