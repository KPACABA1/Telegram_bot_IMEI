from django.apps import AppConfig
from django.core.signals import Signal


class ImeiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'imei'
