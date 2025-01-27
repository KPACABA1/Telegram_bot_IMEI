from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from imei.models import TokenTG


class TokenTGSerializer(ModelSerializer):
    """Сериализатор для моделей контактов."""
    # Проверяю чтобы пользователь ввёл токен и IMEI
    name = serializers.CharField()
    imei = serializers.CharField(max_length=15)

    def validate_name(self, value):
        """Метод проверяет что поле name существует, если нет, то вызывается ошибка"""
        if not TokenTG.objects.filter(name=value).exists():
            raise serializers.ValidationError('Неправильно введён токен')
        return value

    def validate_imei(self, value):
        """Метод проверяет что поле imei соответствует данным которые должны быть введены"""
        if len(value) > 8 and len(value) < 15 and value.isdigit():
            return value
        raise serializers.ValidationError("IMEI должен быть от 8 до 15 символов и состоять только из цифр!")


    class Meta:
        model = TokenTG
        fields = '__all__'