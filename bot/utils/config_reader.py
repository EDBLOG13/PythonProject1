import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
    DEFAULT_LANG = os.getenv("DEFAULT_LANG", "ru")
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

config = Config()
