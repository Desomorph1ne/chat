import os
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import openai

# Получите токен вашего бота в Telegram и установите его как переменную окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Получите ваш API ключ для OpenAI и установите его как переменную окружения
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Настройка API OpenAI
openai.api_key = OPENAI_API_KEY

# Создайте экземпляр Telegram бота
bot = telegram.Bot(token=BOT_TOKEN)

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я готов отвечать на твои сообщения.")

# Обработчик текстовых сообщений
def generate_response(update, context):
    # Получите текст сообщения от пользователя
    user_message = update.message.text
    
    # Вызовите API OpenAI для генерации ответа
    response = openai.Completion.create(
        engine="davinci", prompt=user_message, max_tokens=50
    )
    
    # Получите ответ из API OpenAI и отправьте его пользователю
    bot_response = response.choices[0].text.strip()
    context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)

# Создайте экземпляр Updater для вашего бота
updater = Updater(token=BOT_TOKEN, use_context=True)

# Добавьте обработчики команд и текстовых сообщений
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_response))

# Запустите бота
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    updater.start_webhook(listen="0.0.0.0", port=port, url_path=BOT_TOKEN)
    updater.bot.setWebhook("https://chatbot-telegram.herokuapp.com/" + BOT_TOKEN)
    updater.idle()
