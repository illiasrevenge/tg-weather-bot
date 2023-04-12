# Here we store telegram handlers
from processors.responses import Responses
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CallbackContext


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
        print('handle message')
        text = str(update.message.text).lower()
        user_id = str(update.message.from_user.id)

        response = self.responses.sample_response(text, user_id)
        await update.message.reply_text(response)

    async def handle_location(self, update: Update, context):
        print(update)
        if update is not None:
            location = update.message.location
            user_id = str(update.message.from_user.id)

            response = await self.responses.handle_location(user_id, str(location.latitude),
                                                           str(location.longitude))
        else:
            response = 'Error'

        await update.message.reply_text(response)

    async def handle_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update causes the following error {context.error}')

    async def __callback_alarm(self, context: ContextTypes.DEFAULT_TYPE):
        # Beep the person who called this alarm:
        await context.bot.send_message(chat_id=context.job.chat_id, text=f'BEEP {context.job.data}!')

    async def callback_timer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        name = update.effective_chat.full_name
        await context.bot.send_message(chat_id=chat_id, text='Setting a timer for 1 minute!')
        # Set the alarm:
        context.job_queue.run_once(self.__callback_alarm, 5, data=name, chat_id=chat_id)
