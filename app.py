from flask import Flask
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import Config
from karma import Karma
import redis
import json
import random

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
            parameters = update.message.text.split(" ")[2:]
            if len(parameters) < 3:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Add Quote Format: /q add USERNAME QUOTE")
            else:
                username = parameters[0]
                quotation = " ".join(parameters[1:])
                if r.exists(f"user:{username}") == 0:
                    quotation = json.dumps(quotation)
                    r.hset(f"user:{username}", "quotes", quotation)
                else:
                    uquotes = r.hget(f"user:{username}", "quotes")
                    if '[' in uquotes:
                        uquotes = json.loads(uquotes)
                    if isinstance(uquotes, list):
                        uquotes.append(quotation)
                        uquotes = json.dumps(uquotes)
                        r.hset(f"user:{username}", "quotes", uquotes)
                        print(uquotes)
                    else:
                        newList = [uquotes, quotation]
                        newList = json.dumps(newList)
                        r.hset(f"user:{username}", "quotes", newList)
                print(r.hget(f"user:{username}", "quotes"))
                context.bot.send_message(chat_id=update.effective_chat.id, text='"'+quotation+'" added to '+username+'\'s quotes!')
    elif r.exists(f"user:{args[0]}") != 0:
        uquotes = r.hget(f"user:{args[0]}", "quotes")
        print(uquotes)
        if '[' in uquotes:
            uquotes = json.loads(uquotes)
            size = len(uquotes)
            index = random.randint(0, size-1)
            uquotes = uquotes[index]
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{args[0]} : {uquotes}")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{args[0]} : {uquotes}")
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