import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

# Загрузка токена из .env файла
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Инициализация Flask и Telegram
app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

# Инициализация диспетчера
dispatcher = Dispatcher(bot, None, workers=0)

# URL вашего веб-приложения
WEB_APP_URL = "https://<ваш-домен>.vercel.app"

# Обработчик команды /start
def start(update, context):
    """Ответ на команду /start"""
    update.message.reply_text(
        f"Добро пожаловать в Новошахтинский драматический театр! "
        f"Перейдите по ссылке, чтобы посетить наш сайт: {WEB_APP_URL}"
    )

# Регистрация обработчика команды /start
dispatcher.add_handler(CommandHandler("start", start))

# Обработчик для всех остальных сообщений
def unknown(update, context):
    update.message.reply_text("Я понимаю только команду /start.")

# Регистрация обработчика неизвестных команд
dispatcher.add_handler(MessageHandler(Filters.command | Filters.text, unknown))

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработка запросов от Telegram"""
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)
