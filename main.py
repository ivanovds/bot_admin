import os
import time
import telebot
from flask import Flask, request

from tg_bot import config, bot

server = Flask(__name__)


bot.remove_webhook()
time.sleep(1)


@server.route('/' + config.BOT_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200


@server.route("/reset_webhook")
def webhook():
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=config.APP_URL_HEROKU + config.BOT_TOKEN, max_connections=100)
    return "OK", 200


@server.route("/")
def home():
    return "OK", 200


if __name__ == "__main__":
    from tg_bot.message_handlers import *
    from monitoring.clock import *
    from monitoring.scale import *

    if config.USE_WEBHOOK:
        bot.set_webhook(url=config.APP_URL_HEROKU + config.BOT_TOKEN, max_connections=100)
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    else:
        bot.polling()
