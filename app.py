from flask import Flask
app = Flask(__name__)
from telegram.ext import Updater, CommandHandler
import logging

TOKEN = '1235895745:AAGGubtpiZnSzEUwbDGFRZvnXOiD237WI5I'

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s-%(name)s-%(messages)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

if __name__ == '__main__':
    updater.start_polling()
    app.run()