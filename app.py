from flask import Flask
app = Flask(__name__)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import Config
import logging
import redis

TOKEN = Config.TOKEN

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s-%(name)s-%(messages)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def add_sub_karma(user, value):
    if r.exists(user) == 0:
        r.set(user, value)
    else:
        karma = int(r.get(user))
        karma = karma + value
        r.set(user, karma)


def karma(string, chat, bot):
    if "++" in string:
        user = string.split("++")[0]
        add_sub_karma(user, 1)
    elif "—" in string:
        user = string.split("—")[0]
        add_sub_karma(user, -1)
    karma = r.get(user) 
    bot.send_message(chat_id=chat.id, text=user+" has "+karma+" karma")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def parse_incoming_message(update, context):
    if "++" or "—" in update.message.text:
        karma(update.message.text, update.effective_chat, context.bot)


messageParse_handler = MessageHandler(Filters.text & (~Filters.command), parse_incoming_message)
dispatcher.add_handler(messageParse_handler)


if __name__ == '__main__':
    updater.start_polling()
    app.run()