import logging
import os
from distutils.util import strtobool
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv("config.env")

# Your Bot token from @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "6206599982:AAGqJ84tpTzhdKYzNRMp2kPdcpN0_1zz5K4")

# Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "16743442"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "12bbd720f4097ba7713c5e40a11dfd2a")

# ID of your Database Channel
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001905486162"))

# Your Name as the Bot Owner
OWNER = os.environ.get("OWNER", "GenXNano")

# Database URL
DB_URI = os.environ.get("DATABASE_URL", "postgres://bzqineqa:we3PTgJrRUxYZXp5iUI8ByKRPDJYi25r@floppy.db.elephantsql.com/bzqineqa")

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

try:
    ADMINS = [int(x) for x in (os.environ.get("ADMINS", "6198858059").split())]
except ValueError:
    raise Exception("Your Admin list does not contain valid Telegram User IDs.")

LOG_FILE_NAME = "logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
