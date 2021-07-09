import time

import requests
from apscheduler.schedulers.background import BackgroundScheduler

import config
from tg_bot.utils import notify_monitoring_chat


ping_yourself = BackgroundScheduler()
ping_prod_ua_bot = BackgroundScheduler()


@ping_yourself.scheduled_job('interval', minutes=5)
def ping_yourself_func():
    response = requests.request("GET", config.APP_URL_HEROKU)
    print(f'SCHEDULED_JOB: APP ping every 5 minutes: {response.text}')

    if response.status_code != 200:
        err_msg = '🆘 ERR ping_yourself_func: bot_admin APP is not responding!'
        print(err_msg)
        notify_monitoring_chat(err_msg)


ping_yourself.start()


@ping_prod_ua_bot.scheduled_job('interval', minutes=1)
def ping_prod_ua_bot_func():
    response = requests.request("GET", config.UA_BOT_URL_HEROKU)
    print(f'SCHEDULED_JOB: PROD APP ping every 1 minute: {response.text}')

    if response.status_code != 200:
        err_msg = '🆘 ERR ping_prod_ua_bot_func: UA bot APP is not responding!'
        print(err_msg)
        notify_monitoring_chat(err_msg)


if config.ENVIRONMENT == 'PROD':
    if config.UA_BOT_URL_HEROKU is None:
        notify_monitoring_chat('🆘 UA_BOT_URL_HEROKU is not set up in heroku config!')
    else:
        ping_prod_ua_bot.start()
