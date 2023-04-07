import os

import constants
import responses as responses
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    variants = [[KeyboardButton(request_location=True, text="🗺️ Відправити геолокацію")]]

    await update.message.reply_text("Привіт, відправ мені геолокацію і дізнайся чи потрібно тобі брати парасолю зараз",
                                    reply_markup=ReplyKeyboardMarkup(variants,
                                                                     one_time_keyboard=True,
                                                                     input_field_placeholder="Відправ геолокацію"
                                                                     )
                                    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("No help is implemented now")


async def handle_message(update: Update, context):
    text = str(update.message.text).lower()

    response = responses.sample_response(text)

    print(f'User ({update.message.chat.id}) in {update.message.chat.type}: {text}')
    await update.message.reply_text(response)


async def handle_location(update: Update, context):
    print(update.message.location)
    location = update.message.location

    response = await responses.handle_location(str(location.latitude), str(location.longitude))

    await update.message.reply_text(response)


if __name__ == '__main__':
    print("Bot has started...")

    app = Application.builder().token(constants.API_KEY).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    app.run_webhook(listen="0.0.0.0",
                    port=int(os.environ.get('PORT', 5000)),
                    url_path=constants.API_KEY,
                    webhook_url= + constants.API_KEY)
