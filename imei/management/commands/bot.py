import os
import requests
import json
import django
from telegram import Update
from telegram.ext import (Application, CommandHandler, MessageHandler, ContextTypes, filters)
from dotenv import load_dotenv
from django.core.management.base import BaseCommand

load_dotenv()

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Токен от бота и белый список пользователей
BOT_TOKEN = os.getenv('BOT_TOKEN')
white_list = os.getenv('white_list')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start с проверкой на то что пользователь в белом списке"""
    if str(update.effective_user.id) in white_list:
        await update.message.reply_text("Привет! Я ваш бот. Напишите что-нибудь!")
    else:
        await update.message.reply_text("Привет! У вас нет прав для доступа к этому боту!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений с проверкой правильности написания IMEI и возвращением информации о нём"""
    user_message = update.message.text
    if len(user_message) > 8 and len(user_message) < 15 and user_message.isdigit():

        # подключение к сервису https://imeicheck.net/
        url = 'https://api.imeicheck.net/v1/checks'
        token_imeicheck = os.getenv('token_imeicheck')
        headers = {
            'Authorization': 'Bearer ' + token_imeicheck,
            'Content-Type': 'application/json'
        }
        body = json.dumps({
            "deviceId": user_message,
            "serviceId": 12
        })
        response = requests.post(url, headers=headers, data=body)

        # Отправляем ответ пользователю если он в белом списке
        if str(update.effective_user.id) in white_list:
            await update.message.reply_text(response.json()['properties'])
        else:
            await update.message.reply_text("У вас нет прав доступа к данному боту")
    else:
        await update.message.reply_text("IMEI должен быть от 8 до 15 символов и состоять только из цифр!")


class Command(BaseCommand):
    """Запускает бота Telegram с использованием Long Polling"""
    def handle(self, *args, **options):
        # Создаём объект Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Регистрация обработчиков
        application.add_handler(CommandHandler("start", start))  # Обработчик команды /start
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))  # Обработчик текстовых сообщений

        # Запуск Long Polling
        print("Бот запущен (Long Polling). Нажмите Ctrl+C для остановки.")
        application.run_polling()
