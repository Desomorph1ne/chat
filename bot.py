import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

# Замените "YOUR_BOT_TOKEN" на токен вашего бота
bot = telegram.Bot(token='BOT_TOKEN')

# Функция для отправки запроса к API ChatGPT и получения ответа
def get_response(message):
    # Замените "YOUR_API_KEY" на ваш API ключ, который вы получили на openai.com
    response = requests.post("https://api.openai.com/v1/engines/davinci-codex/completions",
                             headers={
                                 "Authorization": f"Bearer OPENAI_API_KEY",
                                 "Content-Type": "application/json"
                             },
                             json={
                                 "prompt": message,
                                 "max_tokens": 50,
                                 "temperature": 0.7,
                                 "top_p": 1,
                                 "frequency_penalty": 0,
                                 "presence_penalty": 0
                             })

    return response.json()['choices'][0]['text']

# Обработчик команд
def start(update, context):
    update.message.reply_text('Привет! Я - ваш личный бот, который готов ответить на ваши вопросы!')

def help(update, context):
    update.message.reply_text('Просто отправьте мне сообщение, и я постараюсь ответить на ваш вопрос.')

# Обработчик сообщений от пользователя
def handle_message(update, context):
    message = update.message.text

    # Отправляем сообщение пользователя на обработку в API ChatGPT
    response = get_response(message)

    # Отправляем ответ пользователю в Telegram
    update.message.reply_text(response)

# Настройка обработчиков для бота
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

# Назначение обработчиков для команд и сообщений
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Запуск бота
updater.start_polling()
