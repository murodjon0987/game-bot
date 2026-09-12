import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "8378747437:AAEUDpOAq9ASY63BYgw3oYOggvEJ0eAfHws").strip()
if not BOT_TOKEN:
    BOT_TOKEN = "8378747437:AAEUDpOAq9ASY63BYgw3oYOggvEJ0eAfHws"

# Admin IDs list
admin_ids_raw = os.getenv("ADMIN_IDS", "0").split(",")
ADMIN_IDS = [int(i.strip()) for i in admin_ids_raw if i.strip().isdigit()]

# Admin Telegram username (@username)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "@wenzone72").strip()
if ADMIN_USERNAME and not ADMIN_USERNAME.startswith("@"):
    ADMIN_USERNAME = f"@{ADMIN_USERNAME}"

# Server port for Render.com
PORT = int(os.getenv("PORT", "10000"))

# Database path
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = DATA_DIR / "games.db"

# Available game and app categories with emojis
CATEGORIES = {
    "vip_mod": "💎 VIP & Cheksiz Coins (MOD)",
    "action": "🔥 Jangari (Action)",
    "racing": "🏎 Poyga (Racing)",
    "simulator": "🚗 Simulyator & Avto",
    "puzzle": "🧩 Mantiqiy (Puzzle)",
    "sport": "⚽ Sport",
    "adventure": "🏝 Sarguzasht (Adventure)",
    "retro": "🕹 Retro & Arkada",
    "apps_video": "🎬 Video & Foto Montaj (PRO)",
    "apps_media": "🎵 Musiqa & Media (Premium)",
    "apps_vpn": "⚡️ Tezkor VPN & Xavfsizlik",
    "apps_tools": "🛠 Foydali Dasturlar & AI"
}

GAME_CATEGORIES = ["vip_mod", "action", "racing", "simulator", "puzzle", "sport", "adventure", "retro"]
APP_CATEGORIES = ["apps_video", "apps_media", "apps_vpn", "apps_tools"]
