from functools import wraps
import requests

from tg_bot import bot
import config

error_report_to_chat = '🆘 Error with: %s'


def restart_all_dynos():
    headers = {"Accept": "application/vnd.heroku+json; version=3",
               "Content-Type": "application/json",
               "Authorization": f"Bearer {config.THIS_BOT_API_KEY}"}

    requests.delete('https://api.heroku.com/apps/bots-admin/dynos',
                    headers=headers)


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
        notify_monitoring_chat(err_msg)
        return False


# Feedback chat notifications:
def notify_monitoring_chat(message, document=False, caption='', markdown=False):
    try:
        if not document:
            if markdown:
                bot.send_message(chat_id=config.MONITORING_CHAT_ID,
                                 text=message,
                                 )
            else:
                bot.send_message(chat_id=config.MONITORING_CHAT_ID,
                                 text=message,
                                 )
        else:
            bot.send_document(chat_id=config.MONITORING_CHAT_ID,
                              data=message,
                              caption=caption
                              )

        return True
    except Exception as err:
        print(f'ERR notify_monitoring_chat: {err}')
        return False
