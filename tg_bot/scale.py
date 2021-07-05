import base64
import json

import requests

from config import UA_BOT_HEROKU_API_KEY

# Generate Base64 encoded API Key
BASEKEY = base64.b64encode((":" + UA_BOT_HEROKU_API_KEY).encode("utf-8"))
# Create headers for API call
HEADERS = {"Accept": "application/vnd.heroku+json; version=3", "Authorization": BASEKEY}


def scale_dynos(app_name, process_name, num):
    payload = {"quantity": num}
    json_payload = json.dumps(payload)
    url = f"https://api.heroku.com/apps/{app_name}/formation/{process_name}"
    try:
        result = requests.patch(url, headers=HEADERS, data=json_payload)
    except Exception as e:
        print(f"scale_dynos: {e}")
        return False

    if result.status_code == 200:
        return True

    return False


def get_current_dyno_quantity(app_name, process_name):
    """
    to receive app_name: app_url.replace("https://", "").replace(".herokuapp.com/", "")
    """
    url = f"https://api.heroku.com/apps/{app_name}/formation/"
    print(url)
    try:
        result = requests.get(url, headers=HEADERS)
        for formation in json.loads(result.text):
            if formation["type"] == process_name:
                current_quantity = formation["quantity"]
                return current_quantity
    except Exception as e:
        print(f"get_current_dyno_quantity: {e}")
