import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = json.loads(os.getenv("ADMIN_IDS", "[]"))
