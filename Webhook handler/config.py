import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")
ADMIN_IDS = [12345678, 87654321]  # Replace with actual IDs
DATABASE_PATH = "efootball.db"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") # For Katabump/VPS
PORT = int(os.environ.get('PORT', 5000))

# Settings
ROOM_CODE_REGEX = r'^\d{8}$'
EXPIRE_TIME = 3600  # 1 Hour
