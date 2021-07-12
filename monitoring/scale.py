import time
import json
import threading
import requests

import config
from tg_bot.utils import notify_monitoring_chat

FREE_SIZE = 'Free'
STANDARD_SIZE = 'standard-1x'


class BotMonitor(threading.Thread):

    def __init__(self, bot_token, bot_url_heroku, bot_heroku_auth_token, process_name):
        threading.Thread.__init__(self)
        self.heroku_app_name = bot_url_heroku.replace("https://", "").replace(".herokuapp.com/", "")
        self.bot_token = bot_token
        self.process_name = process_name
        self.pending_update_count = 0
        self.current_dyno_quantity = 0
        self.headers = {"Accept": "application/vnd.heroku+json; version=3"}
        self.bot_heroku_auth_token = bot_heroku_auth_token

        self.shutdown_flag = threading.Event()

    def run(self):
        while not self.shutdown_flag.is_set():
            time.sleep(1)
            print('while')  # TEMP

            bot_info = get_webhook_info(self.bot_token)
            self.pending_update_count = bot_info["pending_update_count"]
            if self.pending_update_count >= config.SCALE_ONCE_PENDING_UPDATE_COUNT:
                msg = f"{self.heroku_app_name} reached or exceeded " \
                      f"SCALE_ONCE_PENDING_UPDATE_COUNT({config.SCALE_ONCE_PENDING_UPDATE_COUNT}) — " \
                      f"{self.pending_update_count}\nwebhook_info: {bot_info}\n\nStarting to scale..."
                print(msg)
                notify_monitoring_chat(msg)

                self.scaling_up_handler()

            elif self.pending_update_count >= config.ALERT_PENDING_UPDATE_COUNT:
                msg = f"{self.heroku_app_name} reached or exceeded " \
                      f"ALERT_PENDING_UPDATE_COUNT({config.ALERT_PENDING_UPDATE_COUNT}) — " \
                      f"{self.pending_update_count}\nwebhook_info: {bot_info}\n\nCheck bot!"
                print(msg)
                notify_monitoring_chat(msg)

    def scaling_up_handler(self):
        self.current_dyno_quantity = self.get_current_dyno_quantity() if not None else 0  # None if no dyno

        new_dyno_quantity = None
        new_size = None
        if self.pending_update_count > config.SCALE_TWICE_PENDING_UPDATE_COUNT and (
                self.current_dyno_quantity != config.MAX_DYNO_QUANTITY):  # +2
            new_dyno_quantity = min(self.current_dyno_quantity + 2, config.MAX_DYNO_QUANTITY)
            new_size = STANDARD_SIZE
        elif self.current_dyno_quantity is None:
            new_dyno_quantity = 1
            new_size = FREE_SIZE
        elif self.current_dyno_quantity in [i for i in range(1, config.MAX_DYNO_QUANTITY)]:  # +1
            new_dyno_quantity = self.current_dyno_quantity + 1  # up to MAX_DYNO_QUANTITY
            new_size = STANDARD_SIZE
        elif self.current_dyno_quantity == config.MAX_DYNO_QUANTITY:
            msg = f"🆘 {self.heroku_app_name} reached MAX_DYNOS={config.MAX_DYNO_QUANTITY} " \
                  f"but has {self.pending_update_count} of pending_update_count!\n\nDo something ASAP!!!"
            print(msg)
            notify_monitoring_chat(msg)
            time.sleep(10)

        if None not in [new_size, new_dyno_quantity]:
            self.scale_dynos(new_dyno_quantity=new_dyno_quantity, new_size=new_size)

    def scaling_down_handler(self):  # TODO: implement
        pass

    def get_current_dyno_quantity(self):
        url = f"https://api.heroku.com/apps/{self.heroku_app_name}/formation/"
        try:
            result = requests.get(url, headers=self.headers, auth=('', self.bot_heroku_auth_token))
            print(result.json())
            if result.ok:
                for formation in json.loads(result.text):
                    if formation["type"] == self.process_name:
                        current_quantity = formation["quantity"]
                        return current_quantity
            else:
                err_msg = f"ERR_1 get_current_dyno_quantity: {result.text}"
                print(err_msg)
                notify_monitoring_chat(err_msg)
        except Exception as err:
            err_msg = f"ERR_2 get_current_dyno_quantity: {err}"
            print(err_msg)
            notify_monitoring_chat(err_msg)

    def scale_dynos(self, new_dyno_quantity, new_size):
        payload = {"quantity": new_dyno_quantity, "size": new_size}
        json_payload = json.dumps(payload)
        url = f"https://api.heroku.com/apps/{self.heroku_app_name}/formation/{self.process_name}"
        try:
            result = requests.patch(url, headers=self.headers, data=json_payload,
                                    auth=('', self.bot_heroku_auth_token))
        except Exception as e:
            err_msg = f"ERR scale_dynos: {e}"
            print(err_msg)
            notify_monitoring_chat(err_msg)
            return False

        if result.status_code == 200:
            msg = f"Scaled from {self.current_dyno_quantity} to {new_dyno_quantity} dynos!\n\nresult: {result.json()}"
            print(msg)
            notify_monitoring_chat(msg)

            time.sleep(60)  # TODO: do smth better

            return True
        else:
            err_msg = f"ERR scale_dynos: failed to scale.\nresult: {result.text}"
            print(err_msg)
            notify_monitoring_chat(err_msg)
            return False

    def stop(self):
        self.shutdown_flag.set()


def get_webhook_info(bot_token):
    try:
        tg_bot_info = requests.get(f"https://api.telegram.org/bot{bot_token}/getWebhookInfo")
        if tg_bot_info is not None:
            tg_bot_info = tg_bot_info.json()

            if tg_bot_info["ok"]:
                keep_keys = {
                    "last_error_date", "last_error_message", "max_connections", "allowed_updates",
                    "pending_update_count"
                }
                return {key: value for key, value in tg_bot_info["result"].items() if key in keep_keys}
            else:
                err_msg = f"ERR_1 get_webhook_info: Status not 'ok'\ntg_bot_info: {tg_bot_info}"
                print(err_msg)
                notify_monitoring_chat(err_msg)
        else:
            err_msg = "ERR_2 get_webhook_info: tg_bot_info is None"
            print(err_msg)
            notify_monitoring_chat(err_msg)
    except Exception as err:
        err_msg = f"ERR_3 get_webhook_info: {err}"
        print(err_msg)
        notify_monitoring_chat(err_msg)


ua_bot_monitor = BotMonitor(bot_token=config.UA_BOT_TOKEN,
                            bot_url_heroku=config.UA_BOT_URL_HEROKU,
                            bot_heroku_auth_token=config.UA_BOT_HEROKU_AUTH_TOKEN,
                            process_name=config.BOT_MAIN_PROCESS)
ua_bot_monitor.start()
