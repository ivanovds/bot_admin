import time
import base64
import json
import threading
import requests

import config
from tg_bot.utils import notify_monitoring_chat


class BotMonitor(threading.Thread):

    def __init__(self, bot_token, bot_url_heroku, bot_heroku_api_key, process_name):
        threading.Thread.__init__(self)
        self.heroku_app_name = bot_url_heroku.replace("https://", "").replace(".herokuapp.com/", "")
        self.bot_token = bot_token
        self.process_name = process_name
        self.pending_update_count = 0
        # Generate Base64 encoded API Key
        base_key = base64.b64encode((":" + bot_heroku_api_key).encode("utf-8"))
        # Create headers for API call
        self.headers = {"Accept": "application/vnd.heroku+json; version=3", "Authorization": base_key}

        self.shutdown_flag = threading.Event()

    def run(self):
        while not self.shutdown_flag.is_set():
            time.sleep(1)

            bot_info = get_webhook_info(self.bot_token)
            self.pending_update_count = bot_info["pending_update_count"]
            if self.pending_update_count >= config.MAX_PENDING_UPDATE_COUNT:
                msg = f"{self.heroku_app_name} reached or exceeded " \
                      f"MAX_PENDING_UPDATE_COUNT({config.MAX_PENDING_UPDATE_COUNT}) — " \
                      f"{self.pending_update_count}\nwebhook_info: {bot_info}\n\nScale it ASAP!!!"
                print(msg)
                notify_monitoring_chat(msg)

                # self.scaling_handler()  TODO: implement

                time.sleep(60)  # TEMP

            elif self.pending_update_count >= config.ALERT_PENDING_UPDATE_COUNT:
                msg = f"{self.heroku_app_name} reached or exceeded " \
                      f"ALERT_PENDING_UPDATE_COUNT({config.ALERT_PENDING_UPDATE_COUNT}) — " \
                      f"{self.pending_update_count}\nwebhook_info: {bot_info}\n\nCheck bot!"
                print(msg)
                notify_monitoring_chat(msg)

                time.sleep(60)  # TEMP

    def scaling_handler(self):
        current_dyno_quantity = self.get_current_dyno_quantity()  # None if no dyno
        print("current_dyno_quantity=", current_dyno_quantity)

        new_dyno_quantity = self.get_new_dyno_quantity()
        success = self.scale_dynos(new_dyno_quantity=new_dyno_quantity)

        if success:
            msg = f"Scaled from {current_dyno_quantity} to {new_dyno_quantity} dynos!"
            print(msg)
            notify_monitoring_chat(msg)

    def get_new_dyno_quantity(self):
        return 2  # TODO: implement

    def get_current_dyno_quantity(self):
        url = f"https://api.heroku.com/apps/{self.heroku_app_name}/formation/"
        try:
            result = requests.get(url, headers=self.headers)
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

    def scale_dynos(self, new_dyno_quantity):
        payload = {"quantity": new_dyno_quantity}
        json_payload = json.dumps(payload)
        url = f"https://api.heroku.com/apps/{self.heroku_app_name}/formation/{self.process_name}"
        try:
            result = requests.patch(url, headers=self.headers, data=json_payload)
        except Exception as e:
            err_msg = f"ERR scale_dynos: {e}"
            print(err_msg)
            notify_monitoring_chat(err_msg)
            return False

        if result.status_code == 200:
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


ua_bot_monitor = BotMonitor(bot_token=config.UA_BOT_TOKEN, bot_url_heroku=config.UA_BOT_URL_HEROKU,
                            bot_heroku_api_key=config.UA_BOT_HEROKU_API_KEY, process_name=config.BOT_MAIN_PROCESS)
ua_bot_monitor.start()
