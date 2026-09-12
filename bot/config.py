import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Admin IDs list
admin_ids_raw = os.getenv("ADMIN_IDS", "0").split(",")
ADMIN_IDS = [int(i.strip()) for i in admin_ids_raw if i.strip().isdigit()]

# Server port for Render.com
PORT = int(os.getenv("PORT", "10000"))

# Database path
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = DATA_DIR / "games.db"

# Available game categories with emojis
CATEGORIES = {
    "action": "🔥 Jangari (Action)",
    "racing": "🏎 Poyga (Racing)",
    "puzzle": "🧩 Mantiqiy (Puzzle)",
    "sport": "⚽ Sport",
    "adventure": "🏝 Sarguzasht (Adventure)",
    "retro": "🕹 Retro & Arkada"
}
