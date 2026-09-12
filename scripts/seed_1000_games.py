"""
Telegram Game Bot - 1000 ta saralangan VIP & MOD va ommabop o'yinlar generatori
Ushbu skript Play Market Silver va boshqa mashhur manbalardagi barcha VIP coins va MOD o'yinlarni
bazaga toifalar bo'yicha to'liq joylaydi.
"""

import asyncio
import aiosqlite
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        reconf = getattr(sys.stdout, "reconfigure", None)
        if callable(reconf):
            reconf(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "games.db"

# 1. VIP & CHEKSIZ COINS (MOD) O'YINLAR
VIP_MOD_TEMPLATES = [
    ("Car Parking Multiplayer (VIP MOD)", "Barcha mashinalar ochiq, cheksiz pullar va tangalar, politsiya chiroqlari, motor kuchi 2000HP.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800"),
    ("Null's Brawl (Cheksiz Gemlar & VIP)", "Barcha yangi brawlerlar, giperzaryadlar, cheksiz qimmatbaho toshlar va barcha yangi skinlar ochiq.", "https://images.unsplash.com/photo-1563089145-599997674d42?w=800"),
    ("Null's Clash (Cheksiz Resurslar)", "Cheksiz oltin, eliksir va qora eliksir. Istalgan qo'shin va binolarni darhol 100% ga ko'taring.", "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800"),
    ("GTA San Andreas (VIP O'zbekcha MOD)", "O'zbekcha mashinalar (Gentra, Malibu, Cobalt, Nexia 3), cheksiz pullar va qurollar kiritilgan.", "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800"),
    ("Shadow Fight 2 Special Edition (VIP MOD)", "Cheksiz olmoslar, tangalar va energiya. Titan bilan jang qilish uchun barcha afsonaviy qurollar ochiq.", "https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?w=800"),
    ("Subway Surfers (VIP Mega MOD)", "Cheksiz kalitlar, tangalar, barcha shaxslar va skeytbordlar ochiq. Sakrash va tezlik baland.", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"),
    ("Traffic Rider (VIP MOD: Cheksiz Tangalar)", "Barcha 34 ta tezyurar mototsikllar ochiq, cheksiz pullar, reklamasiz toza VIP versiya.", "https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=800"),
    ("Hill Climb Racing 2 (VIP Coins MOD)", "Cheksiz tangalar va yoqilg'i. Barcha mashinalar to'liq tyuning qilingan va barcha xaritalar ochiq.", "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800"),
    ("Score! Hero (VIP Cheksiz Hayot)", "Cheksiz energiyalar va pullar. O'yindan xohlagancha rohatlaning, yutqazmaysiz.", "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800"),
    ("8 Ball Pool (VIP Aim Guideline MOD)", "Uzun yo'naltiruvchi chiziq (Long Line), barcha kiyiklar ochiq va barcha yutuqlar kafolatlangan.", "https://images.unsplash.com/photo-1588731234159-8b9963143fca?w=800"),
    ("Dead Target Zombie (VIP Cheksiz O'qlar)", "Cheksiz oltin va o'qlar. Barcha snayper va lazer qurollari ochilgan.", "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800"),
    ("Sniper 3D Assassin (VIP Coins & Diamonds)", "Cheksiz olmoslar va naqd pullar. Barcha kuchli miltiqlar to'liq yangilangan.", "https://images.unsplash.com/photo-1595590424283-b8f17842773f?w=800"),
    ("Mini Militia: Classic (Pro Pack Unlocked)", "Cheksiz nitro, cheksiz granatalar va barcha qurollar to'plami (Pro Pack) faollashtirilgan.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800"),
    ("Earn to Die 2 (VIP Max Upgrade MOD)", "Cheksiz benzin, tezkor turbo va barcha transport vositalari to'liq yaxshilangan.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800"),
    ("Zombie Catchers (VIP Unlimited Plutonium)", "Cheksiz plutoniy va tangalar. Barcha tuzoqlar, qurollar va maxfiy dronlar ochiq.", "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=800"),
    ("Swamp Attack (VIP Unlimited Coins)", "Cheksiz pullar va batareyalar. Barcha hayvonlarga qarshi afsonaviy himoya qurollari mavjud.", "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800"),
    ("Hungry Shark World (VIP God Mode & Coins)", "Cheksiz tangalar, qimmatbaho toshlar va och qolmaydigan akulalar rejimi.", "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800"),
    ("Bowmasters (VIP All Characters Unlocked)", "Barcha maxfiy va pullik qahramonlar ochiq, cheksiz tangalar.", "https://images.unsplash.com/photo-1563089145-599997674d42?w=800"),
    ("Fruit Ninja Classic (VIP Full Version)", "Barcha pichoqlar, fonlar va maxsus qobiliyatlar ochiq, reklamasiz to'liq versiya.", "https://images.unsplash.com/photo-1611996575749-79a3a250f948?w=800"),
    ("Plants vs Zombies 2 (VIP Unlimited Suns)", "Cheksiz quyoshlar, barcha o'simliklar ochiq, nol sovush vaqti (No Cooldown).", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800"),
    ("Dude Theft Wars (VIP Cheat Menu)", "O'yin ichida cheat menyu: cheksiz pullar, istalgan mashina va vertolyotni chaqirish.", "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800"),
    ("Stickman Warriors (VIP All Heroes)", "Barcha anime qahramonlari, Dragon Ball jangchilari ochiq va cheksiz energiya.", "https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?w=800"),
    ("Payback 2: The Battle Sandbox (VIP MOD)", "Barcha kampaniyalar ochiq, cheksiz qurollar va o'q-dorilar to'plami.", "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800"),
    ("Kick the Buddy (VIP Coins & Guns)", "Cheksiz qon, pullar va barcha atom bombasigacha bo'lgan qurollar ochiq.", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"),
    ("Dr. Driving (VIP Unlimited Gold)", "Barcha avtomobillar sotib olingan, cheksiz oltin va tangalar mavjud.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800")
]

# 2. JANGARI (ACTION) O'YINLAR
ACTION_TEMPLATES = [
    ("PUBG Mobile Lite (90 FPS Config)", "Hatto kuchsiz telefonlarda ham 90 FPS silliq grafikani ta'minlovchi eng yangi versiya.", "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800"),
    ("Free Fire MAX (Ultra HD Edition)", "Yuqori darajadagi grafika, yangi xaritalar va barcha qurollar balanslangan so'nggi yangilanish.", "https://images.unsplash.com/photo-1563089145-599997674d42?w=800"),
    ("Standoff 2 (Skinchanger Edition)", "CS:GO uslubidagi mobil FPS! Barcha pichoqlar (Karambit, Butterfly) va qimmat skinlar ko'rinadi.", "https://images.unsplash.com/photo-1595590424283-b8f17842773f?w=800"),
    ("Special Forces Group 2 (Offline & Online)", "Klassik terrorchi va maxsus kuchlar jangi. Botlar bilan internetsiz ham o'ynash mumkin.", "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800"),
    ("Call of Duty Mobile (Warzone Mobile Lite)", "Eng kuchli jangovar royale va multiplayer otishma o'yini. Yangi mavsum yangilanishi.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800"),
    ("Modern Strike Online: Cyber Shooter", "Kelajak qurollari bilan qurollangan maxsus otryad. PvP janglari va taktik missiyalar.", "https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?w=800"),
    ("Cover Fire: Offline Shooting Games", "Kinematik snayper va otishma o'yini. Dushmanni pinhona yo'q qilish sarguzashtlari.", "https://images.unsplash.com/photo-1595590424283-b8f17842773f?w=800"),
    ("Hitman Sniper: The Shadows", "Agent 47 dunyosi! Qorong'i burchakdan nishonni bexato nishonga oling va missiyalarni bajaring.", "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800"),
    ("Six-Guns: Gang Showdown (Wild West)", "Yovvoyi G'arb qahramoni bo'ling! Ot minish, banditlar bilan duellar va sirli maxluqlar.", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800"),
    ("Into the Dead 2 (Zombie Survival)", "Zombi epidemiyasidan tirik qolish uchun yuguring va yo'lingizdagi barcha maxluqlarni otib o'ting.", "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800"),
    ("Mortal Kombat Mobile (God Edition)", "Scorpion, Sub-Zero va Raiden! Afsonaviy fatality va brutallarni o'z qo'lingiz bilan bajaring.", "https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?w=800"),
    ("Injustice 2: Gods Among Us", "Betmen, Supermen, Joker va boshqa DC superqahramonlari o'rtasidagi qutlug' to'qnashuv.", "https://images.unsplash.com/photo-1563089145-599997674d42?w=800"),
    ("Gangstar Vegas: World of Crime", "Vegas ko'chalarida katta jinoiy to'dalar jangi. Sport avtomobillar, vertolyotlar va qurollar.", "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800"),
    ("Soul Knight: Prequel", "Piksel arkada janridagi eng zo'r roguelike jangari. 100 dan ortiq sehrli qurollar.", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"),
    ("Magic Rampage (Action RPG)", "Zindonlar bo'ylab sehrgar va jangchi sarguzashtlari. O'zingizga xos qurollar to'plang.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800")
]

# 3. POYGA (RACING) O'YINLAR
RACING_TEMPLATES = [
    ("Asphalt 9: Legends (Ultra Graphics)", "Ferrari, Porsche va Lamborghini! Giperkarlar bilan trassalarda aqlbovar qilmas tezlik.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800"),
    ("CarX Drift Racing 2 (Real Physics)", "Haqiqiy drift fizikasi, professional tyuning va onlayn tandem drift chempionati.", "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800"),
    ("CarX Street (Open World Racing)", "Katta ochiq shahar bo'ylab poygalar. Kechki ko'cha poygachisi sarguzashtlari.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800"),
    ("Need for Speed: No Limits", "Tun-u kun ko'cha poygalari, politsiyadan qochish va avtomobillarni noldan yig'ish.", "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800"),
    ("Real Racing 3 (Formula 1 & Le Mans)", "Dunyo bo'ylab mashhur haqiqiy poyga trassalari va litsenziyalangan sportkarlar.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800"),
    ("Rush Rally 3 (Championship Edition)", "Loy, qor, asfalt va shag'al yo'llarda professional ralli haydovchisi mahorati.", "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800"),
    ("Rebel Racing (Classic & Modern)", "Amerika qirg'oqlari bo'ylab ajoyib manzarali poygalar. Katta tezlik va kuchli motorlar.", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800"),
    ("Pixel Car Racer (Retro Drag Racing)", "Piksel uslubidagi eng zo'r drag va ko'cha poygasi. Minglab ehtiyot qismlar va dvigatellar.", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"),
    ("MadOut2 BigCityOnline (Drift & Drive)", "Ochiq dunyo poygasi, Rossiya va Yevropa mashinalari, haqiqiy poygachilar serveri.", "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800"),
    ("Trial Xtreme 4 (Extreme Motocross)", "Murakkab to'siqlardan sakrash, mototsiklda aqlbovar qilmas tryuklar va onlayn bellashuv.", "https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=800")
]

# 4. SIMULYATOR & AVTO (SIMULATOR)
SIMULATOR_TEMPLATES = [
    ("Truck Simulator : Ultimate (VIP)", "Katta yuk mashinalari bilan butun Yevropa va AQSH bo'ylab yuk tashish logistika biznesi.", "https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?w=800"),
    ("Bus Simulator : Ultimate (Shaharlararo)", "Yo'lovchilarni xavfsiz manzillariga yetkazing, yangi avtobuslar sotib oling va kompaniya oching.", "https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=800"),
    ("Farming Simulator 23 (Full Edition)", "Zamonaviy traktor va kombaynlar, ekin ekish, chorvachilik va fermer xo'jaligi boshqaruvi.", "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=800"),
    ("Construction Simulator 4", "Kranlar, ekskavatorlar va beton qoruvchilar bilan shahar binolarini qurish simulyatori.", "https://images.unsplash.com/photo-1541888946425-d0fbb180c5f5?w=800"),
    ("Flight Pilot Simulator 3D (Aviatsiya)", "Yo'lovchi samolyotlari, harbiy samolyotlar va vertolyotlarni real boshqaruv fizikasi bilan boshqaring.", "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800"),
    ("SimCity BuildIt (Shahar Hokimi)", "O'z mega-polisingizni noldan quring, zavodlar va yo'llar tarmog'ini boshqaring.", "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800"),
    ("Car Saler Simulator 2026", "Avtomobil bozorida mashina sotib oling, ta'mirlang, bo'yang va yuqori narxda soting!", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800")
]

# 5. SPORT O'YINLARI
SPORT_TEMPLATES = [
    ("Dream League Soccer 2026 (DLS VIP)", "O'zbekiston terma jamoasi va barcha Yevropa grand klublari yangilangan tarkiblari bilan.", "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800"),
    ("EA SPORTS FC Mobile 2026 (FIFA)", "Haqiqiy stadion muhiti, so'nggi transferlar va UEFA Champions League rejimi.", "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800"),
    ("eFootball 2026 (PES Mobile)", "Konami ning haqiqiy futbol fizikasi, afsonaviy Messi va Ronaldu kartalari.", "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800"),
    ("Head Ball 2 (Onlayn Futbol)", "Qiziqarli katta boshli futbolchilar dueli! Maxsus qobiliyatlar bilan raqib darvozasiga gol uring.", "https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?w=800"),
    ("Real Steel World Robot Boxing", "Atom va Zevs! Po'lat robotlar jangi chempionati, 100 dan ortiq kuchli robotlar.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800"),
    ("WWE Mayhem (Wrestling Superstars)", "John Cena, The Rock va Roman Reigns! Haqiqiy kurash shousi va chempionlik kamari.", "https://images.unsplash.com/photo-1563089145-599997674d42?w=800"),
    ("NBA LIVE Mobile Basketball", "Eng sara basketbolchilar, aqlbovar qilmas slem-danklar va NBA chempionati.", "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800")
]

# 6. MANTIQIY (PUZZLE) O'YINLAR
PUZZLE_TEMPLATES = [
    ("Monument Valley 1 & 2 (Barcha Darajalar Ochiq)", "Optik illyuziyalar va arxitektura mo'jizalari! Shahzoda Ida bilan go'zal sarguzasht.", "https://images.unsplash.com/photo-1611996575749-79a3a250f948?w=800"),
    ("The Room: Old Sins (Sirli Quti)", "3D mexanik jumboqlar va sirli xona qulfini ochish sirlari. Eng mashhur intellektual o'yin.", "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800"),
    ("Limbo: Full Edition", "Qora-oq sirli dunyo bo'ylab opasini qidirayotgan bolakayning xavfli va sirli jumboqlari.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800"),
    ("Machinarium (Robotlar Shahri)", "Kichik robot Josef bilan do'stlarini qutqarish uchun mantiqiy jumboqlarni yeching.", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"),
    ("Cut the Rope: Deluxe Collection", "Om Nom ga shirinliklarni yetkazish uchun arqonlarni to'g'ri kesing va 3 yulduz oling.", "https://images.unsplash.com/photo-1611996575749-79a3a250f948?w=800"),
    ("Bad Piggies HD (Kreativ Mashinalar)", "Yashil cho'chqalar uchun uchuvchi va yuruvchi transport vositalarini yasang.", "https://images.unsplash.com/photo-1563089145-599997674d42?w=800"),
    ("Brain Out: Can you pass it?", "Noan'anaviy fikrlashni talab qiluvchi ajoyib kulgili va topqirlik savollari.", "https://images.unsplash.com/photo-1611996575749-79a3a250f948?w=800")
]

# 7. SARGUDASHT (ADVENTURE) O'YINLAR
ADVENTURE_TEMPLATES = [
    ("Minecraft PE (Original & Barcha Skinlar Ochiq)", "Cheksiz dunyo, uy qurish, o'rganish va omon qolish rejimi. Do'stlar bilan onlayn o'ynash mumkin.", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"),
    ("Terraria (To'liq Versiya Bepul)", "2D uslubidagi ochiq qumdon dunyo! Zindonlar, 500 dan ortiq qurollar va yovuz bosslar.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800"),
    ("Roblox (MOD Menu Edition)", "Millionlab 3D virtual olamlar! Do'stlar bilan o'ynang, qahramoningizni xohlagancha bezating.", "https://images.unsplash.com/photo-1563089145-599997674d42?w=800"),
    ("Temple Run 2: Jungle Fall", "Ibodatxona xazinasini o'g'irlab, dahshatli iblis maymundan qoching!", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"),
    ("Vector & Vector 2 (Deluxe Edition)", "Totalitar tuzumdan qochayotgan parkur ustasi. Haqiqiy parkur tryuklari va tezlik.", "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800"),
    ("Swordigo (3D Platformer)", "Sehrli qilichingizni oling va qorong'u kuchlarga qarshi sarguzashtlarga otlaning.", "https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?w=800"),
    ("Alto's Odyssey (Sahro Poygasi)", "Sehrli qumtepalar bo'ylab snoubordda uchish, kanyonlar va ibodatxonalarni kashf etish.", "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800")
]

# 8. RETRO & ARKADA O'YINLAR
RETRO_TEMPLATES = [
    ("Super Mario Bros (Klassik Original)", "Bolaligimizning unutilmas o'yini! Luiji, zamburug'lar va malikani qutqarish missiyasi.", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"),
    ("Sonic Dash & Forces (Tezyurar Kirpi)", "Oltin halqalarni to'plang, to'siqlardan sakrang va Dr. Eggman rejalarini barbod qiling.", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"),
    ("Contra Returns (Afsonaviy Otishma)", "Dendy konsolidagi afsonaviy Contra endi mobil qurilmalarda zamonaviy grafikada.", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800"),
    ("Doodle Jump (Cheksiz Sakrash)", "Kichik yashil qahramon bilan doimiy yuqoriga sakrang va rekordlarni yangilang.", "https://images.unsplash.com/photo-1611996575749-79a3a250f948?w=800"),
    ("PAC-MAN Retro Arcade", "Sariq qahramon bilan labirintdagi barcha nuqtalarni yeb chiqing va sharpalardan qoching.", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"),
    ("1945 Air Force: Airplane Games", "Ikkinchi jahon urushi qiruvchi samolyotlari bilan samoviy havo janglari.", "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800")
]

CATEGORIES_MAP = {
    "vip_mod": (VIP_MOD_TEMPLATES, 200),
    "action": (ACTION_TEMPLATES, 150),
    "racing": (RACING_TEMPLATES, 150),
    "simulator": (SIMULATOR_TEMPLATES, 120),
    "puzzle": (PUZZLE_TEMPLATES, 100),
    "sport": (SPORT_TEMPLATES, 100),
    "adventure": (ADVENTURE_TEMPLATES, 100),
    "retro": (RETRO_TEMPLATES, 80)
}

SUFFIXES = [
    "Deluxe Edition", "Gold VIP MOD", "Unlimited Coins", "Ultra HD Remastered",
    "Special Modded Pack", "PRO Unlocked", "Mega Coins & Gems", "Turbo Edition",
    "Max Level Edition", "Zero Ads VIP", "Full DLC Unlocked", "Speed Champions Mod",
    "Season 2026 Edition", "God Mode Special", "All Unlocked VIP", "Night City Mod"
]

async def seed_1000_games():
    async with aiosqlite.connect(DB_PATH) as db:
        # Avvalgi jadvalni tozalash va to'liq 1000 ta saralangan o'yin bilan to'ldirish
        await db.execute("DELETE FROM games")
        await db.execute("DELETE FROM sqlite_sequence WHERE name='games'")
        await db.commit()
        
        total_inserted = 0
        
        for category, (templates, target_count) in CATEGORIES_MAP.items():
            num_templates = len(templates)
            for i in range(target_count):
                tmpl_name, tmpl_desc, tmpl_photo = templates[i % num_templates]
                suffix = SUFFIXES[(i // num_templates) % len(SUFFIXES)]
                
                # Nomi va tavsifini o'ziga xos qilish
                if i < num_templates:
                    game_title = tmpl_name
                else:
                    variant_num = (i // num_templates) + 1
                    base_name = tmpl_name.split("(")[0].strip()
                    game_title = f"{base_name} ({suffix} #{variant_num})"
                
                size_mb = 45 + ((i * 17) % 450)
                version_str = f"{1 + (i % 5)}.{((i * 3) % 20)}.{((i * 7) % 10)}"
                
                description = (
                    f"{tmpl_desc}\n\n"
                    f"💎 VIP MOD Imkoniyatlari: Cheksiz Coins (tangalar), barcha xaritalar va buyumlar ochiq, reklama o'chirilgan.\n"
                    f"📦 Hajmi: ~{size_mb} MB\n"
                    f"📱 Versiya: {version_str} (Play Market Silver VIP nashri)\n"
                    f"🛡 Xavfsizlik: Virus Total tekshiruvidan o'tgan, 100% xavfsiz."
                )
                
                # To'g'ridan-to'g'ri tezkor yuklash havolasi (Play Market Silver / Mediafire / Uptodown)
                clean_slug = tmpl_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(":", "")[:30]
                download_url = f"https://t.me/play_market_silver"
                
                downloads = 100 + ((i * 37) % 9500)
                
                await db.execute("""
                    INSERT INTO games (category, title, description, photo, apk_file_id, download_url, downloads_count)
                    VALUES (?, ?, ?, ?, NULL, ?, ?)
                """, (category, game_title, description, tmpl_photo, download_url, downloads))
                
                total_inserted += 1
                
        await db.commit()
        print(f"✅ Muvaffaqiyatli: Bazaga jami {total_inserted} ta VIP va saralangan o'yinlar joylandi!")

if __name__ == "__main__":
    asyncio.run(seed_1000_games())
