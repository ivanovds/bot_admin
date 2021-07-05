import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USE_WEBHOOK = True

BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_URL_HEROKU = os.environ.get("APP_URL_HEROKU")
ENVIRONMENT = os.environ.get("ENVIRONMENT", None)  # "DEV"/"TEST"/"PROD"

# DBP = f"host={os.environ.get("DB_HOST")} dbname={os.environ.get("DB_NAME")} user={os.environ.get("DB_USER")}" \
#       f" password={os.environ.get("DB_PASSWORD")}  connect_timeout=3"


ADMIN_ID = 298760372
USERS = [ADMIN_ID, 301327435]
FEEDBACK_CHAT_ID = os.environ.get("FEEDBACK_CHAT_ID")


UA_BOT_URL_HEROKU = os.environ.get("UA_BOT_URL_HEROKU", None)  # PROD bot
UA_BOT_TOKEN = os.environ.get("UA_BOT_TOKEN")
UA_BOT_HEROKU_API_KEY = os.environ.get("UA_BOT_HEROKU_API_KEY")
UA_BOT_MAIN_PROCESS = os.environ.get("UA_BOT_MAIN_PROCESS", "web")


MAX_PENDING_UPDATE_COUNT = int(os.environ.get("MAX_PENDING_UPDATE_COUNT", 5))

if os.path.isfile("./config_user.py"):
    from config_user import *
