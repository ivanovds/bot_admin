import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USE_WEBHOOK = True

BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_URL_HEROKU = os.environ.get("APP_URL_HEROKU")
ENVIRONMENT = os.environ.get("ENVIRONMENT", None)  # "DEV"/"TEST"/"PROD"
LANDING_URL_HEROKU = os.environ.get("LANDING_URL_HEROKU", 'https://corona-travel-bot.herokuapp.com/')
API_KEY = os.environ.get("API_KEY", None)

# DBP = f"host={os.environ.get("DB_HOST")} dbname={os.environ.get("DB_NAME")} user={os.environ.get("DB_USER")}" \
#       f" password={os.environ.get("DB_PASSWORD")}  connect_timeout=3"


ADMIN_ID = 298760372
USERS = [ADMIN_ID]
MONITORING_CHAT_ID = os.environ.get("MONITORING_CHAT_ID")


BOT_MAIN_PROCESS = os.environ.get("UA_BOT_MAIN_PROCESS", "web")
ALERT_PENDING_UPDATE_COUNT = int(os.environ.get("ALERT_PENDING_UPDATE_COUNT", 3))
SCALE_ONCE_PENDING_UPDATE_COUNT = int(os.environ.get("SCALE_ONCE_PENDING_UPDATE_COUNT", 5))
SCALE_TWICE_PENDING_UPDATE_COUNT = int(os.environ.get("SCALE_TWICE_PENDING_UPDATE_COUNT", 100))
MAX_DYNO_QUANTITY = int(os.environ.get("MAX_DYNO_QUANTITY", 4))  # 4dyno * 21threads = 84+ database connections
SECONDS_TO_WAIT_BEFORE_SCALING_DOWN = int(os.environ.get("SECONDS_TO_WAIT_BEFORE_SCALING_DOWN", 300))


# Bots to be monitored:
UA_BOT_URL_HEROKU = os.environ.get("UA_BOT_URL_HEROKU", None)
UA_BOT_TOKEN = os.environ.get("UA_BOT_TOKEN")
UA_BOT_HEROKU_AUTH_TOKEN = os.environ.get("UA_BOT_HEROKU_AUTH_TOKEN")


if os.path.isfile("./config_user.py"):
    from config_user import *
