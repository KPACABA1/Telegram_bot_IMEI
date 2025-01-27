# botapp/management/commands/bot.py

import os
from os.path import exists

import django
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from asgiref.sync import sync_to_async  # Импортируем sync_to_async

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Укажите путь к вашим настройкам
django.setup()

from imei.models import TokenTG  # Импорт моделей Django

BOT_TOKEN = '7798011301:AAEcr2h266eKErzcwfN-9E8yWKx1VFf48Jc'

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я ваш бот. Напишите что-нибудь!")

# Обработчик текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    # Проверяем, существует ли объект с pk=1
    exists = await sync_to_async(TokenTG.objects.filter(name='1').exists)()

    if exists:
        await update.message.reply_text("Объект с pk=1 существует!")
    else:
        await update.message.reply_text("Объект с pk=1 не найден.")

    # # Отправляем ответ пользователю
    # await update.message.reply_text(f"Вы написали: {user_message}")

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Запускает бота Telegram с использованием Long Polling'

    def handle(self, *args, **options):
        # Создаём объект Application (новая замена Updater)
        application = Application.builder().token(BOT_TOKEN).build()

        # Регистрация обработчиков
        application.add_handler(CommandHandler("start", start))  # Обработчик команды /start
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))  # Обработчик текстовых сообщений

        # Запуск Long Polling
        print("Бот запущен (Long Polling). Нажмите Ctrl+C для остановки.")
        application.run_polling()
