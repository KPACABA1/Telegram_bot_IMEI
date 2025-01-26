from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from imei.models import TokenTG


class TokenTGSerializer(ModelSerializer):
    """Сериализатор для моделей контактов."""
    # Проверяю чтобы поле name существовало
    name = serializers.CharField()

    def validate_name(self, value):
        """Метод проверяет что поле name существует, если нет, то вызывается ошибка"""
        if not TokenTG.objects.filter(name=value).exists():
            raise serializers.ValidationError(f'Неправильно введён токен')
        return value

    class Meta:
        model = TokenTG
        fields = '__all__'