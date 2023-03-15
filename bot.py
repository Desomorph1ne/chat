import os
import telegram
import requests
import openai_secret_manager

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Подключаемся к API Telegram с помощью токена бота
bot = telegram.Bot(token=os.environ['BOT_TOKEN'])

# Получаем ключ API от OpenAI
openai_secrets = openai_secret_manager.get_secret("openai")

# Функция, которая отвечает на сообщения пользователя
def respond(update, context):
    message = update.message.text
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {openai_secrets['api_key']}"
    }
    data = {
        'prompt': message,
        'temperature': 0.5,
        'max_tokens': 100,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }
    response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, json=data)
    completion = response.json()['choices'][0]['text']
    bot.send_message(chat_id=update.message.chat_id, text=completion)

# Запускаем бота
bot = telegram.Bot(token=os.environ['BOT_TOKEN'])
updater = telegram.ext.Updater(token=os.environ['BOT_TOKEN'], use_context=True)
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command, respond))
updater.start_polling()
