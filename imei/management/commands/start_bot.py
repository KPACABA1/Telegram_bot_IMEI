import asyncio
from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Функция для обработки сообщений
async def echo(update: Update, context: CallbackContext) -> None:
    print(f"Получено сообщение: {update.message.text}")

# Функция для запуска бота
async def start_bot():
    # Токен, который ты получил от BotFather
    TOKEN = '7798011301:AAEcr2h266eKErzcwfN-9E8yWKx1VFf48Jc'

    # Создаем приложение (заменяет Updater)
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем поллинг
    await application.run_polling()

# Основная команда для запуска бота и Django-сервера
class Command(BaseCommand):
    help = 'Запускает Telegram бота и сервер Django'

    def handle(self, *args, **kwargs):
        # Запуск асинхронного кода с помощью asyncio
        loop = asyncio.get_event_loop()

        # Запускаем бота и сервер Django в одном процессе
        self.stdout.write(self.style.SUCCESS('Запуск бота и сервера...'))
        loop.create_task(start_bot())  # Запуск бота
        from django.core.management import call_command
        call_command('runserver')  # Запуск сервера Django