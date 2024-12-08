import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# Загрузка токена из .env файла
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Инициализация Flask
app = Flask(__name__)

# Инициализация бота и приложения
application = Application.builder().token(TELEGRAM_TOKEN).build()

# URL вашего веб-приложения
WEB_APP_URL = "https://<ваш-домен>.vercel.app"

# Обработчик корневого маршрута
@app.route('/')
def home():
    return 'Привет! Ваш бот работает.'

# Обработчик команды /start
async def start(update: Update, context):
    """Ответ на команду /start"""
    await update.message.reply_text(
        f"Добро пожаловать в Новошахтинский драматический театр! "
        f"Перейдите по ссылке, чтобы посетить наш сайт: {WEB_APP_URL}"
    )

# Регистрация обработчика команды /start
application.add_handler(CommandHandler("start", start))

# Обработчик для всех остальных сообщений
async def unknown(update: Update, context):
    await update.message.reply_text("Я понимаю только команду /start.")

# Регистрация обработчика неизвестных команд
application.add_handler(MessageHandler(filters.COMMAND | filters.TEXT, unknown))

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработка запросов от Telegram"""
    json_str = request.get_json(force=True)
    update = Update.de_json(json_str, application.bot)
    application.update_queue.put(update)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)
