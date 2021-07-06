"""
Handlers for all non standard incoming messages
"""
import os


from tg_bot import bot, dict_text
from tg_bot import reply_markup as rm
from .utils import (
    is_admin, notify_admin, message_user_access,
    message_admin_access, get_webhook_info,
    notify_monitoring_chat,
)


@bot.message_handler(commands=['start'])
@message_user_access()
def start_command(message, cancel_message=False):
    if cancel_message:
        msg = dict_text.canceled
    else:
        msg = dict_text.start_inline_menu

    bot.send_message(message.from_user.id, msg)


@bot.message_handler(commands=['help'])
@message_user_access()
def help_command(message):
    bot.send_message(chat_id=message.from_user.id,
                     text=dict_text.help_text,
                     disable_web_page_preview=True)


@bot.message_handler(regexp=f'^{dict_text.b_cancel}$')
@message_user_access()
def canceled(message):
    start_command(message, cancel_message=True)


@bot.message_handler(commands=['ua_webhook_info'])
@message_user_access()
def get_webhook_info_command(message):
    text = str(get_webhook_info())
    bot.send_message(chat_id=message.from_user.id,
                     text=text,
                     disable_web_page_preview=True)


@bot.message_handler(commands=['test'])
@message_admin_access()
def test_command(message):
    notify_monitoring_chat('test')
    print('ok')


@bot.message_handler(content_types=["text", "photo", "document"])
def general_con(message):
    start_command(message)



