"""
Handlers for all non standard incoming messages
"""
import time
import config
from tg_bot import bot, dict_text
from .utils import (
    message_user_access,
    message_admin_access, )
from monitoring.scale import get_webhook_info, BotMonitor


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


@bot.message_handler(commands=['ua_start_monitoring'])
@message_user_access()
def get_webhook_info_command(message):
    from monitoring.scale import ua_bot_monitor
    ua_bot_monitor.stop()
    time.sleep(1)
    ua_bot_monitor.start()

    bot.send_message(chat_id=message.from_user.id,
                     text='Monitoring successfully (re)started!')


@bot.message_handler(commands=['ua_stop_monitoring'])
@message_user_access()
def get_webhook_info_command(message):
    from monitoring.scale import ua_bot_monitor
    ua_bot_monitor.stop()
    bot.send_message(chat_id=message.from_user.id,
                     text='Monitoring successfully stopped!')


@bot.message_handler(commands=['test'])
@message_admin_access()
def test_command(message):
    from monitoring.scale import BotMonitor
    ua_bot_monitor = BotMonitor(bot_token=config.UA_BOT_TOKEN,
                                bot_url_heroku=config.UA_BOT_URL_HEROKU,
                                bot_heroku_auth_token=config.UA_BOT_HEROKU_AUTH_TOKEN,
                                process_name=config.BOT_MAIN_PROCESS)

    current_dyno_quantity = ua_bot_monitor.get_current_dyno_quantity()

    print(current_dyno_quantity)


@bot.message_handler(content_types=["text", "photo", "document"])
def general_con(message):
    start_command(message)
