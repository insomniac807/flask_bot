from flask import Flask
from karma import Karma
app = Flask(__name__)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import Config
import redis

TOKEN = Config.TOKEN

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def parse_incoming_message(update, context):
    if "++" in update.message.text or "—" in update.message.text or update.message.text.split(" ")[0] == "karma":
        karma = Karma(r)
        karma.handle_karma(update.message.text, update.effective_chat, context.bot)


messageParse_handler = MessageHandler(Filters.text & (~Filters.command), parse_incoming_message)
dispatcher.add_handler(messageParse_handler)


if __name__ == '__main__':
    updater.start_polling()
    app.run()