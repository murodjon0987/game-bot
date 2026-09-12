import sqlite3
from pathlib import Path

db_path = Path("data/games.db")
if db_path.exists():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE games SET download_url = NULL WHERE download_url LIKE '%t.me/%' OR download_url LIKE '%telegram%'")
    conn.commit()
    print("Cleaned games rows:", c.rowcount)
    conn.close()
