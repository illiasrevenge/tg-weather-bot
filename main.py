import constants
from handlers.message_handlers import MessageHandlers
from telegram.ext import Application, CommandHandler, MessageHandler, Updater, filters


if __name__ == '__main__':
    # Telegram bot related stuff
    app = Application.builder().token(constants.API_KEY).build()
    handlers = MessageHandlers()

    app.add_handler(CommandHandler('start', handlers.start_command))
    app.add_handler(CommandHandler('test', handlers.callback_timer))
    app.add_handler(MessageHandler(filters.TEXT, handlers.handle_message))
    app.add_handler(MessageHandler(filters.LOCATION, handlers.handle_location))

    # app.add_error_handler(handlers.handle_error)

    app.run_polling()
