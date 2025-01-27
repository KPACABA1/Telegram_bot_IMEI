import os

import django
from telegram import Update
from telegram.ext import (Application, CommandHandler, MessageHandler, ContextTypes, filters)
from asgiref.sync import sync_to_async
from imei.models import TokenTG
from dotenv import load_dotenv
from django.core.management.base import BaseCommand

load_dotenv()

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    await update.message.reply_text("Привет! Я ваш бот. Напишите что-нибудь!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    user_message = update.message.text

    # Проверяем, существует ли объект с pk=1
    exists = await sync_to_async(TokenTG.objects.filter(pk=1).exists)()

    if exists:
        print('1')
    else:
        print('2')

    # Отправляем ответ пользователю
    await update.message.reply_text(f"вы написал - {user_message}")


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
