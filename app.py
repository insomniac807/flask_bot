from flask import Flask
app = Flask(__name__)
import telegram
bot = telegram.Bot(token='1235895745:AAGGubtpiZnSzEUwbDGFRZvnXOiD237WI5I')


@app.route('/')
def hello():
    mybot = str(bot.get_me())
    return "Hello World!"+mybot

if __name__ == '__main__':
    app.run()