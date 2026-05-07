import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("8721581472:AAEL4QKl_AoJ2caDhp9nBJxJODa-iAhBP-o", #"YOUR_TOKEN_HERE")
ADMIN_IDS = [8551276141]  # Replace with actual IDs
DATABASE_PATH = "efootball.db"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") # For Katabump/VPS
PORT = int(os.environ.get('PORT', 5000))

# Settings
ROOM_CODE_REGEX = r'^\d{8}$'
EXPIRE_TIME = 3600  # 1 Hour
