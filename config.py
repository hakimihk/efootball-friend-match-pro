import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = "8721581472:AAEL4QKl_AoJ2caDhp9nBJxJODa-iAhBP-o"
ADMIN_IDS = [8551276141]
DATABASE_PATH = "efootball.db"  # Line-kan ayaa kuu dhimman!

# Settings-ka kale
WEBHOOK_URL = "https://example.onrender.com/"
PORT = int(os.environ.get('PORT', 5000))
