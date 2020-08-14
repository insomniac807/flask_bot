from flask import Flask
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import Config
from karma import Karma
import redis
import json

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
        if args[0].lower() == "add":
            list = update.message.text.split(" ")[2:]
            if len(list) < 3:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Add Quote Format: /q add USERNAME QUOTE")
            else:
                username = list[0]
                quotation = json.dumps(" ".join(list[1:]))
                print(f"user:{username}")
                if r.exists(f"user:{username}") != 0:
                    r.hset(f"user:{username}", "quotes", quotation)
                    i = 1
                    i += 1
                context.bot.send_message(chat_id=update.effective_chat.id, text='"'+quotation+'" added to '+username+'\'s quotes!')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Second parameter looks dodgy there pal <.<")

quote_handler = CommandHandler('q', quote)
dispatcher.add_handler(quote_handler)
###################################################################################################################################################

def parse_incoming_message(update, context):
    if "++" in update.message.text or "—" in update.message.text or update.message.text.split(" ")[0] == "karma":
        if not update.message.via_bot == "None":
            karma = Karma(r)
            karma.handle_karma(update.message.text.lower(), update.effective_chat, context.bot)


messageParse_handler = MessageHandler(Filters.text & (~Filters.command), parse_incoming_message)
dispatcher.add_handler(messageParse_handler)


if __name__ == '__main__':
    updater.start_polling()
    app.run()