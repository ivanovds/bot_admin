import time

import requests
from apscheduler.schedulers.background import BackgroundScheduler

import config
from tg_bot.utils import notify_monitoring_chat


ping_yourself = BackgroundScheduler()
ping_prod_ua_bot = BackgroundScheduler()
ping_landing = BackgroundScheduler()

ping_prod_molfar = BackgroundScheduler()


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


@ping_landing.scheduled_job('interval', minutes=10)
def ping_landing_func():
    response = requests.request("GET", config.LANDING_URL_HEROKU)
    print(f'SCHEDULED_JOB: Landing ping every 10 minutes: {response.status_code}')

    if response.status_code != 200:
        err_msg = '🆘 ERR ping_landing_func: UA bot APP is not responding!'
        print(err_msg)
        notify_monitoring_chat(err_msg)


@ping_prod_molfar.scheduled_job('interval', minutes=3)
def ping_prod_molfar_func():
    """Molfar (army-tickets) project"""

    response = requests.request("GET", config.MOLFAR_BE_URL_HEROKU)
    print(f'SCHEDULED_JOB: Molfar Backend ping every 3 minutes: {response.text}')

    if response.status_code != 200:
        err_msg = '🆘 ERR ping_prod_molfar_func: Molfar (Backend) is not responding!'
        print(err_msg)
        notify_monitoring_chat(err_msg)

    response = requests.request("GET", config.MOLFAR_FE_URL_HEROKU)
    print(f'SCHEDULED_JOB: Molfar Frontend ping every 3 minutes: {response.text}')

    if response.status_code != 200:
        err_msg = '🆘 ERR ping_prod_molfar_func: Molfar (Frontend) is not responding!'
        print(err_msg)
        notify_monitoring_chat(err_msg)


if config.ENVIRONMENT == 'PROD':
    if config.UA_BOT_URL_HEROKU is None:
        notify_monitoring_chat('🆘 UA_BOT_URL_HEROKU is not set up in heroku config!')
    else:
        ping_prod_ua_bot.start()
