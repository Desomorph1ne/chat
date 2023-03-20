import logging
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Замените на ваш API-ключ OpenAI и API-ключ Telegram

# Настройка OpenAI API
openai.api_key = OPENAI_API_KEY

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Обработчик для команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Я ваш бот на основе GPT-3.')

# Обработчик для текстовых сообщений
def echo(update: Update, context: CallbackContext):
    user_text = update.message.text
    ai_response = generate_ai_response(user_text)
    update.message.reply_text(ai_response)

# Функция для генерации ответа с помощью GPT-3
def generate_ai_response(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    ai_response = response.choices[0].text.strip()
    return ai_response

def main():
    # Создайте объект Updater и передайте токен API
    updater = Updater(TELEGRAM_API_KEY, use_context=True)

    # Получите диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Регистрация обработчиков
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запустите бот
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

