from functools import wraps
import telebot

from tg_bot import bot
import config

error_report_to_chat = '🆘 Error with: %s'


def is_admin(user_id):
    if user_id == config.ADMIN_ID:
        return True
    else:
        return False


def is_user(user_id):
    if user_id in config.USERS:
        return True
    else:
        return False


def message_user_access():
    """
    Restrict access to the command to users allowed by the is_user function.
    """
    def deco_restrict(f):

        @wraps(f)
        def f_restrict(message, *args, **kwargs):
            user_id = message.from_user.id

            if is_user(user_id):
                return f(message, *args, **kwargs)
            else:
                return

        return f_restrict  # true decorator

    return deco_restrict


def message_admin_access():
    """
    Restrict access to the command to users allowed by the is_admin function.
    """
    def deco_restrict(f):

        @wraps(f)
        def f_restrict(message, *args, **kwargs):
            user_id = message.from_user.id

            if is_admin(user_id):
                return f(message, *args, **kwargs)
            else:
                return

        return f_restrict  # true decorator

    return deco_restrict


# ######## Notifications block ########
# Admin notifications:
def notify_admin(message):
    try:
        bot.send_message(chat_id=config.ADMIN_ID,
                         text=message,
                         )
        return True
    except Exception as err:
        err_msg = error_report_to_chat % f'ERR notify_admin: {err}'
        print(err_msg)
        notify_feedback_chat(err_msg)
        return False


# Feedback chat notifications:
def notify_feedback_chat(message, document=False, caption='', markdown=False):
    try:
        if not document:
            if markdown:
                bot.send_message(chat_id=config.FEEDBACK_CHAT_ID,
                                 text=message,
                                 )
            else:
                bot.send_message(chat_id=config.FEEDBACK_CHAT_ID,
                                 text=message,
                                 )
        else:
            bot.send_document(chat_id=config.FEEDBACK_CHAT_ID,
                              data=message,
                              caption=caption
                              )

        return True
    except Exception as err:
        print(f'ERR notify_feedback_chat: {err}')
        return False


def get_webhook_info():
    tg_bot = telebot.TeleBot(config.UA_BOT_TOKEN)
    tg_bot_info = tg_bot.get_webhook_info()

    return {
        'last_error_date': tg_bot_info['last_error_date'],
        'last_error_message': tg_bot_info['last_error_message'],
        'max_connections': tg_bot_info['max_connections'],
        'allowed_updates': tg_bot_info['allowed_updates'],
        'pending_update_count': tg_bot_info['pending_update_count'],
    }
