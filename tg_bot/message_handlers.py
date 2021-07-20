"""
Handlers for all non standard incoming messages
"""
import time
import config
from tg_bot import bot, dict_text
from .utils import (
    message_user_access,
    message_admin_access, )
from monitoring.scale import get_webhook_info, ua_bot_monitor


@bot.message_handler(commands=['start'])
@message_user_access()
def start_command(message, cancel_message=False):
    if cancel_message:
        msg = dict_text.canceled
    else:
        msg = dict_text.start_inline_menu + f'\n\n{dict_text.help_text}'

    bot.send_message(message.from_user.id, msg)


@bot.message_handler(commands=['help'])
@message_user_access()
def help_command(message):
    bot.send_message(chat_id=message.from_user.id,
                     text=dict_text.help_text,)


@bot.message_handler(commands=['ua_webhook_info'])
@message_user_access()
def get_webhook_info_command(message):
    bot.send_message(chat_id=message.from_user.id,
                     text=str(get_webhook_info(config.UA_BOT_TOKEN)))


@bot.message_handler(commands=['ua_stop_monitoring'])
@message_user_access()
def ua_stop_monitoring_command(message):
    ua_bot_monitor.stop()
    bot.send_message(chat_id=message.from_user.id,
                     text='Monitoring successfully stopped!\n'
                          'To start it again: restart all dynos in Heroku «bots-admin» account.')


@bot.message_handler(commands=['ua_current_dyno_quantity'])
@message_user_access()
def ua_current_dyno_quantity_command(message):
    current_dyno_quantity = ua_bot_monitor.get_current_dyno_quantity()
    bot.send_message(chat_id=message.from_user.id,
                     text=f'ua_current_dyno_quantity: {current_dyno_quantity}')


# @bot.message_handler(commands=['test'])
# @message_admin_access()
# def test_command(message):
#     print('ok')
