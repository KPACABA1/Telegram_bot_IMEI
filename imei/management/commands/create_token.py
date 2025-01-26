from django.core.management import BaseCommand

from imei.models import TokenTG


class Command(BaseCommand):
    """Команда для создания токена."""
    def handle(self, *args, **options):
        token_tg = TokenTG.objects.create(name='1234qwer')
        token_tg.save()