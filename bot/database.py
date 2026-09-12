import aiosqlite
from bot.config import DATABASE_PATH

INITIAL_GAMES = [
    {
        "category": "adventure",
        "title": "Subway Surfers: Zurich",
        "description": "🏃‍♂️ Dunyodagi eng mashhur yugurish o'yini! Poyezdlar ustida yuguring, tangalarni to'plang va inspektordan qoching!\n\n📦 Hajmi: ~135 MB\n📱 Versiya: 3.32.0 (MOD: Cheksiz tangalar/kalitlar)",
        "photo": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800&auto=format&fit=crop",
        "apk_file_id": None,
        "download_url": "https://subway-surfers.en.uptodown.com/android/download"
    },
    {
        "category": "action",
        "title": "Shadow Fight 2",
        "description": "🥋 Ajoyib jang san'ati va sehrli qobiliyatlar uyg'unlashgan afsonaviy jangari o'yin! Barcha shaytonlarni yengib, darvozalarni yoping!\n\n📦 Hajmi: ~145 MB\n📱 Versiya: 2.35.0 (Maxsus nashr)",
        "photo": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&auto=format&fit=crop",
        "apk_file_id": None,
        "download_url": "https://shadow-fight-2.en.uptodown.com/android/download"
    },
    {
        "category": "racing",
        "title": "Traffic Rider",
        "description": "🏍 Shahar bo'ylab tezyurar mototsiklni boshqaring! 1-shaxs nigohi, real dvigatel ovozlari va 30 dan ortiq ajoyib mototsikllar.\n\n📦 Hajmi: ~110 MB\n📱 Versiya: 1.99b (Hamma mototsikllar ochiq)",
        "photo": "https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=800&auto=format&fit=crop",
        "apk_file_id": None,
        "download_url": "https://traffic-rider.en.uptodown.com/android/download"
    },
    {
        "category": "puzzle",
        "title": "2048 & Mantiqiy jumboqlar",
        "description": "🧩 Miya uchun ajoyib gimnastika! Kataklarni suring va 2048 raqamiga erishing. Oddiy qoidalar, ammo chuqur strategiya talab qiladi.\n\n📦 Hajmi: ~15 MB\n📱 Versiya: 4.1.2 (Offline rejim)",
        "photo": "https://images.unsplash.com/photo-1611996575749-79a3a250f948?w=800&auto=format&fit=crop",
        "apk_file_id": None,
        "download_url": "https://2048.en.uptodown.com/android/download"
    },
    {
        "category": "sport",
        "title": "Dream League Soccer (DLS)",
        "description": "⚽ O'z orzuingizdagi futbol jamoasini quring! Haqiqiy litsenziyalangan futbolchilar, ajoyib 3D grafika va onlayn chempionatlar.\n\n📦 Hajmi: ~550 MB\n📱 Versiya: 2026 yangilanishi",
        "photo": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800&auto=format&fit=crop",
        "apk_file_id": None,
        "download_url": "https://dream-league-soccer.en.uptodown.com/android/download"
    },
    {
        "category": "retro",
        "title": "Super Retro Bros (Klassik)",
        "description": "🕹 Bolaligimizning unutilmas retro platformeri! O'sha mashhur musiqa, qo'ziqorinlar va qahramonlik sarguzashtlari endi Androidda.\n\n📦 Hajmi: ~25 MB\n📱 Versiya: Klassik Retro Edition",
        "photo": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800&auto=format&fit=crop",
        "apk_file_id": None,
        "download_url": "https://retro-games.en.uptodown.com/android/download"
    }
]

async def init_db():
    """Ma'lumotlar bazasini initsializatsiya qilish va dastlabki jadvallarni yaratish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                photo TEXT,
                apk_file_id TEXT,
                download_url TEXT,
                downloads_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                invite_link TEXT NOT NULL,
                is_active INTEGER DEFAULT 1
            )
        """)
        await db.commit()
        
        # O'yinlar jadvali bo'shmi? Bo'sh bo'lsa dastlabki o'yinlarni qo'shish
        cursor = await db.execute("SELECT COUNT(*) FROM games")
        count = (await cursor.fetchone())[0]
        if count == 0:
            for game in INITIAL_GAMES:
                await db.execute("""
                    INSERT INTO games (category, title, description, photo, apk_file_id, download_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    game["category"],
                    game["title"],
                    game["description"],
                    game["photo"],
                    game["apk_file_id"],
                    game["download_url"]
                ))
            await db.commit()

async def add_user(user_id: int, full_name: str, username: str | None = None):
    """Foydalanuvchini bazaga qo'shish yoki yangilash"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO users (id, full_name, username)
            VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                full_name = excluded.full_name,
                username = excluded.username
        """, (user_id, full_name, username))
        await db.commit()

async def get_all_users():
    """Barcha foydalanuvchilar ID larini olish (broadcast uchun)"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT id FROM users")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]

async def get_user_count():
    """Foydalanuvchilar sonini hisoblash"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        row = await cursor.fetchone()
        return row[0] if row else 0

async def get_games_by_category(category: str):
    """Kategoriya bo'yicha o'yinlar ro'yxatini olish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT id, title, downloads_count FROM games 
            WHERE category = ? ORDER BY id DESC
        """, (category,))
        return await cursor.fetchall()

async def get_game_by_id(game_id: int):
    """ID bo'yicha bitta o'yin ma'lumotlarini olish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT * FROM games WHERE id = ?
        """, (game_id,))
        return await cursor.fetchone()

async def add_game(category: str, title: str, description: str, photo: str, apk_file_id: str, download_url: str):
    """Yangi o'yin qo'shish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO games (category, title, description, photo, apk_file_id, download_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (category, title, description, photo, apk_file_id, download_url))
        await db.commit()
        return cursor.lastrowid

async def delete_game(game_id: int):
    """O'yinni o'chirish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM games WHERE id = ?", (game_id,))
        await db.commit()

async def search_games(query: str):
    """O'yin nomi bo'yicha qidirish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT id, title, category, downloads_count FROM games 
            WHERE title LIKE ? COLLATE NOCASE
            ORDER BY id DESC LIMIT 20
        """, (f"%{query}%",))
        return await cursor.fetchall()

async def get_random_game():
    """Tasodifiy bitta o'yinni tanlash"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT * FROM games ORDER BY RANDOM() LIMIT 1
        """)
        return await cursor.fetchone()

async def increment_download(game_id: int):
    """O'yin yuklab olinganida uning yuklashlar hisoblagichini oshirish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE games SET downloads_count = downloads_count + 1 WHERE id = ?
        """, (game_id,))
        await db.commit()

async def get_channels():
    """Faol majburiy obuna kanallarini olish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM channels WHERE is_active = 1")
        return await cursor.fetchall()

async def add_channel(chat_id: str, title: str, invite_link: str):
    """Majburiy obuna kanalini qo'shish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO channels (chat_id, title, invite_link)
            VALUES (?, ?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET
                title = excluded.title,
                invite_link = excluded.invite_link,
                is_active = 1
        """, (chat_id, title, invite_link))
        await db.commit()

async def delete_channel(channel_id: int):
    """Kanalni o'chirish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM channels WHERE id = ?", (channel_id,))
        await db.commit()

async def get_stats():
    """Statistika ma'lumotlarini olish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        users_cur = await db.execute("SELECT COUNT(*) FROM users")
        total_users = (await users_cur.fetchone())[0]
        
        games_cur = await db.execute("SELECT COUNT(*), COALESCE(SUM(downloads_count), 0) FROM games")
        games_row = await games_cur.fetchone()
        total_games = games_row[0]
        total_downloads = games_row[1]
        
        channels_cur = await db.execute("SELECT COUNT(*) FROM channels WHERE is_active = 1")
        total_channels = (await channels_cur.fetchone())[0]
        
        return {
            "total_users": total_users,
            "total_games": total_games,
            "total_downloads": total_downloads,
            "total_channels": total_channels
        }
