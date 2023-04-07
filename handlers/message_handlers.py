# Here we store telegram handlers
from processors.responses import Responses
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes


class MessageHandlers:
    responses: Responses

    def __init__(self):
        self.responses = Responses()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        variants = [[KeyboardButton(request_location=True, text="🗺️ Відправити геолокацію")]]

        await update.message.reply_text("Привіт, відправ мені геолокацію і дізнайся чи потрібно тобі брати парасолю зараз",
                                        reply_markup=ReplyKeyboardMarkup(variants,
                                                                         one_time_keyboard=True,
                                                                         input_field_placeholder="Відправ геолокацію"
                                                                         ))

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("No help is implemented now")

    async def handle_message(self, update: Update, context):
        text = str(update.message.text).lower()
        user_id = str(update.message.from_user.id)

        response = self.responses.sample_response(text, user_id)
        await update.message.reply_text(response)

    async def handle_location(self, update: Update, context):
        location = update.message.location
        user_id = str(update.message.from_user.id)

        response = await self.responses.handle_location(user_id, str(location.latitude), str(location.longitude))

        await update.message.reply_text(response)

    async def handle_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update causes the following error {context.error}')
