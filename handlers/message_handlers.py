# Here we store telegram handlers
from processors import responses as responses
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes


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
    location = update.message.location

    response = await responses.handle_location(str(location.latitude), str(location.longitude))

    await update.message.reply_text(response)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update causes the following error {context.error}')
