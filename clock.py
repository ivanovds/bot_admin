import time

import requests
import telebot
from apscheduler.schedulers.background import BackgroundScheduler

import config
from tg_bot.utils import notify_feedback_chat, get_webhook_info

ping_yourself = BackgroundScheduler()
ping_prod_ua_bot = BackgroundScheduler()
monitor_prod_bots_webhook_info = BackgroundScheduler()


@ping_yourself.scheduled_job('interval', minutes=5)
def ping_yourself_func():
    response = requests.request("GET", config.APP_URL_HEROKU)
    print(f'SCHEDULED_JOB: APP ping every 5 minutes: {response.text}')

    if response.status_code != 200:
        err_msg = '🆘 ERR ping_yourself_func: APP is not responding!'
        print(err_msg)
        notify_feedback_chat(err_msg)


ping_yourself.start()


@ping_prod_ua_bot.scheduled_job('interval', minutes=1)
def ping_prod_ua_bot_func():
    response = requests.request("GET", config.UA_BOT_URL_HEROKU)
    print(f'SCHEDULED_JOB: PROD APP ping every 1 minute: {response.text}')

    if response.status_code != 200:
        err_msg = '🆘 ERR ping_prod_ua_bot_func: APP is not responding!'
        print(err_msg)
        notify_feedback_chat(err_msg)


@monitor_prod_bots_webhook_info.scheduled_job('interval', seconds=1)
def monitor_prod_bots_webhook_info_func():

    ua_bot_info = get_webhook_info()
    if ua_bot_info['pending_update_count'] >= config.MAX_PENDING_UPDATE_COUNT:
        msg = f'UA_BOT: pending_update_count >= {config.MAX_PENDING_UPDATE_COUNT}\nwebhook_info: {ua_bot_info}'
        print(msg)
        notify_feedback_chat(msg)

        time.sleep(10)


if config.ENVIRONMENT == 'PROD':
    # do NOT uncomment this while TEST app is pinging!
    # if config.UA_BOT_URL_HEROKU is None:
    #     notify_feedback_chat('🆘 UA_BOT_URL_HEROKU is not set up in heroku config!')
    # else:
    #     ping_prod_ua_bot.start()

    if config.UA_BOT_TOKEN is None:
        notify_feedback_chat('🆘 UA_BOT_TOKEN is not set up in heroku config!')
    else:
        monitor_prod_bots_webhook_info.start()
