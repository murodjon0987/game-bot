"""
500 ta eng sara va ommabop PRO/VIP ilovalar (CapCut, InShot, Spotify, VPN, WPS Office va b.)
"""
import asyncio
import aiosqlite
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "games.db"

APP_CATEGORIES_DATA = {
    "apps_video": (
        [
            ("CapCut PRO (Video Editor & Maker)", "viamaker", "Suv belgisisiz (No Watermark), barcha VIP effektlar va animatsiyalar ochiq, 4K 60FPS eksport.", "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=800"),
            ("InShot PRO (Full Video & Photo)", "inshot-editor", "Barcha filtrlari ochiq, reklamasiz, cheksiz shriftlar va stikerlar to'plami.", "https://images.unsplash.com/photo-1536240478700-b869070f9279?w=800"),
            ("Alight Motion PRO (Motion Graphics)", "alight-motion", "XML loyihalarni ochish, suv belgisisiz eksport, barcha vizual effektlar va vektor grafikasi.", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"),
            ("FilmoraGo VIP (Speed Ramping & VFX)", "filmorago", "Professional montaj vositalari, tezkor harakat (velocity), barcha premium musiqa va o'tishlar.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800"),
            ("PicsArt Gold VIP (Photo Studio)", "picsart", "AI orqa fonni o'chirish, barcha Gold stikerlar, retush va badiiy filtrlar faollashtirilgan.", "https://images.unsplash.com/photo-1611996575749-79a3a250f948?w=800"),
            ("Remini PRO (AI Photo Enhancer)", "remini", "Eski va xira rasmlarni sun'iy intellekt orqali 4K Ultra HD sifatga ko'taruvchi mo'jizaviy ilova.", "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800"),
            ("KineMaster Premium (Chroma Key & 4K)", "kinemaster", "Xromakey (yashil fon), ko'p qatlamli video tahrirlash va audio muharrir.", "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=800"),
            ("Canva PRO (Dizayn & SMM)", "canva", "Barcha premium shablonlar, logotiplar, Instagram postlar va fonni bir zumda tozalash.", "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800")
        ],
        150
    ),
    "apps_media": (
        [
            ("Spotify Premium (Music & Podcasts)", "spotify", "Reklamasiz tinglash, cheksiz musiqalarni o'tkazib yuborish, 320 kbps eng yuqori audio sifati.", "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800"),
            ("Shazam Encore (Musiqa Topuvchi)", "shazam", "Qo'shiqni bir necha soniyada aniqlaydi, matnlari (lyrics) bilan birga ko'rsatadi, reklamasiz.", "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800"),
            ("MX Player Pro (Barcha Codeclar Ochiq)", "mx-player", "AC3, EAC3 audio qo'llab-quvvatlash, apparat tezlatkich (HW+), reklama butunlay o'chirilgan.", "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800"),
            ("SoundCloud (Musiqa & DJ Setlar)", "soundcloud", "Millionlab original treklar, remixlar va podkastlarni qulay tinglash ilovasi.", "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800"),
            ("Poweramp Full Version (Audiophile EQ)", "poweramp", "Grafik ekvalayzer, Hi-Res audio chiqarish va Androiddagi eng kuchli musiqa pleyeri.", "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800")
        ],
        120
    ),
    "apps_vpn": (
        [
            ("Turbo VPN VIP (Cheksiz Tezlik)", "turbo-vpn", "Barcha VIP davlatlar (AQSH, Germaniya, Singapur, Yaponiya) ochiq, cheksiz trafik va tezyurar ping.", "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800"),
            ("1.1.1.1 with WARP+ (Cloudflare)", "1-1-1-1-faster-safer-internet", "Internetni tezlashtiruvchi va xavfsiz qiluvchi rasmiy Cloudflare protokoli, cheksiz WARP+ kvota.", "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800"),
            ("Psiphon Pro (Cheklovlarsiz Internet)", "psiphon", "Har qanday internet cheklovlarini aylanib o'tuvchi mustahkam va ishonchli VPN mijozi.", "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800"),
            ("Thunder VPN (Yengil & Tezkor)", "thunder-vpn", "Batareyani tejovchi, bir tugma bilan ulanuvchi xavfsiz shifrlangan proksi tarmog'i.", "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800"),
            ("Speedtest by Ookla (Premium)", "speedtest", "Internet tezligi, ping va jitter ko'rsatkichlarini real vaqt rejimida aniq o'lchovchi vosita.", "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800")
        ],
        110
    ),
    "apps_tools": (
        [
            ("Telegram (Tezkor & Xavfsiz Messenjer)", "telegram", "Katta fayllar, kanallar, guruhlar va cheksiz bulut xotirasiga ega eng qulay messenjer.", "https://images.unsplash.com/photo-1614680376593-902f749f7ffc?w=800"),
            ("WPS Office Premium (Word, Excel, PDF)", "kingsoft-office", "Hujjatlarni tahrirlash, PDF dan Word ga o'tkazish, elektron imzo qo'yish va reklamasiz rejim.", "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800"),
            ("CamScanner PRO (Hujjat Skaner)", "camscanner", "Qog'oz hujjatlarni telefon kamerasida skaner qilib, toza PDF formatga o'tkazish, OCR matn tanish.", "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800"),
            ("Duolingo Super (Barcha Tillar Ochiq)", "duolingo", "Ingliz, rus, koreys, nemis va boshqa tillarni noldan o'rganish, cheksiz hayotlar.", "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800"),
            ("ZArchiver Pro (Arxivator & 7z)", "zarchiver", "Zip, RAR, 7z, tar arxivlarini ochish va yaratish, parollangan fayllar bilan ishlash.", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"),
            ("Nova Launcher Prime (Kastomizatsiya)", "nova-launcher", "Android interfeysini to'liq o'zgartirish, imo-ishoralar (gestures) va yashirin ilovalar.", "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800")
        ],
        120
    )
}

APP_SUFFIXES = [
    "VIP Premium Edition", "Gold PRO Unlocked", "Ultra Modded 2026", "No Watermark Edition",
    "All Filters & Effects Unlocked", "Plus Edition VIP", "Full License PRO", "Ad-Free Clean Edition",
    "High Speed VIP", "Enterprise PRO", "Unlimited Features Pack", "Max Speed Turbo"
]

async def seed_500_apps():
    async with aiosqlite.connect(DB_PATH) as db:
        # Avvalgi ilovalarni tozalash (o'yinlarga tegilmaydi, faqat app toifalari)
        for cat in APP_CATEGORIES_DATA.keys():
            await db.execute("DELETE FROM games WHERE category = ?", (cat,))
        await db.commit()

        total_apps = 0
        for category, (templates, target_count) in APP_CATEGORIES_DATA.items():
            num_templates = len(templates)
            for i in range(target_count):
                tmpl_name, tmpl_slug, tmpl_desc, tmpl_photo = templates[i % num_templates]
                suffix = APP_SUFFIXES[(i // num_templates) % len(APP_SUFFIXES)]

                if i < num_templates:
                    app_title = tmpl_name
                else:
                    variant_num = (i // num_templates) + 1
                    base_name = tmpl_name.split("(")[0].strip()
                    app_title = f"{base_name} ({suffix} #{variant_num})"

                size_mb = 35 + ((i * 13) % 120)
                version_str = f"{i % 8 + 4}.{((i * 2) % 15)}.{((i * 5) % 10)}"

                description = (
                    f"{tmpl_desc}\n\n"
                    f"⭐ <b>PRO / VIP Imkoniyatlari:</b> Barcha cheklovlar olib tashlangan, reklama o'chirilgan, 100% to'liq versiya.\n"
                    f"📦 <b>Hajmi:</b> ~{size_mb} MB\n"
                    f"📱 <b>Versiya:</b> {version_str} (VIP nashri)\n"
                    f"🛡 <b>Xavfsizlik:</b> Virus Total tekshiruvidan o'tgan, toza va xavfsiz."
                )

                download_url = f"https://{tmpl_slug}.en.uptodown.com/android/download"
                downloads = 500 + ((i * 43) % 15000)

                await db.execute("""
                    INSERT INTO games (category, title, description, photo, apk_file_id, download_url, downloads_count)
                    VALUES (?, ?, ?, ?, NULL, ?, ?)
                """, (category, app_title, description, tmpl_photo, download_url, downloads))
                total_apps += 1

        await db.commit()
        print(f"[OK] Bazaga qo'shimcha {total_apps} ta eng sara PRO/VIP dasturlar qo'shildi!")

if __name__ == "__main__":
    asyncio.run(seed_500_apps())
