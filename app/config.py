# config.py
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.environ.get("ADMIN_IDS", "").split(",")))
