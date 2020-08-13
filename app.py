from flask import Flask
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import Config
from karma import Karma
import redis

app = Flask(__name__)

TOKEN = Config.TOKEN

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

################                       WORKING ON ALL THIS QUOTY STUFF HEREREEREEE ITS EAAASSSYYYYY              #################################
def quote(update, context):
    params = ["add", "search", "delete", "rmlast"]
    args = context.args
    if args[0] in params:
        print(args)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Second parameter looks dodgy there pal <.<")

quote_handler = CommandHandler('q', quote)
dispatcher.add_handler(quote_handler)
###################################################################################################################################################

def parse_incoming_message(update, context):
    if "++" in update.message.text or "—" in update.message.text or update.message.text.split(" ")[0] == "karma":
        karma = Karma(r)
        karma.handle_karma(update.message.text, update.effective_chat, context.bot)


messageParse_handler = MessageHandler(Filters.text & (~Filters.command), parse_incoming_message)
dispatcher.add_handler(messageParse_handler)


if __name__ == '__main__':
    updater.start_polling()
    app.run()