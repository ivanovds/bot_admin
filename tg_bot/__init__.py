import telebot

import config

bot = telebot.TeleBot(config.BOT_TOKEN, threaded=True, num_threads=5)
