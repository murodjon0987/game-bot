# 🎮 Telegram O'yinlar Boti (Game Bot)

Ushbu bot foydalanuvchilarga saralangan qiziqarli Android o'yinlarini toifalar bo'yicha ko'rish, ular haqida to'liq ma'lumot olish, to'g'ridan-to'g'ri Telegram orqali APK faylini yuklash yoki rasmiy tezkor havola orqali yuklab olish imkonini beradi.

Shuningdek botda **majburiy kanallarga obuna tizimi**, qulay **Admin paneli** va **Render.com da 24/7 bepul serverda ishlash** tizimi to'liq sozlangan.

---

## 🌟 Asosiy Imkoniyatlar

1. **Janrlar (Toifalar) bo'yicha saralash**:
   - 🔥 Jangari (Action)
   - 🏎 Poyga (Racing)
   - 🧩 Mantiqiy (Puzzle)
   - ⚽ Sport
   - 🏝 Sarguzasht (Adventure)
   - 🕹 Retro & Arkada
2. **O'yin kartochkasi**:
   - O'yin rasmi (banner)
   - Nomi, janri va yuklab olishlar soni
   - O'yin haqida to'liq ma'lumot, versiyasi va hajmi
   - 📥 **APK faylni Telegram orqali olish**
   - 🌐 **To'g'ridan-to'g'ri tezkor yuklab olish havolasi**
3. **Qidiruv tizimi**:
   - Foydalanuvchi o'yin nomini yozib tezkor qidirishi mumkin.
4. **🎲 Tasodifiy o'yin**:
   - Yangi o'yin qidirayotganlar uchun tasodifiy o'yin tavsiya qiluvchi funksiya.
5. **📢 Majburiy obuna (Mandatory Subscription)**:
   - Foydalanuvchilar botga kirganda homiy kanallarga a'zo bo'lishi talab etiladi.
   - Admin xohlagancha kanal qo'shishi yoki o'chirishi mumkin.
6. **👑 To'liq Admin Panel**:
   - ➕ Yangi o'yin qo'shish (Toifa -> Nom -> Tavsif -> Rasm -> APK fayli yoki havolasi)
   - 🗑 O'yinni o'chirish
   - 📢 Majburiy kanallarni boshqarish
   - 📊 Jonli statistika (Foydalanuvchilar, o'yinlar, yuklashlar)
   - ✉️ Barcha foydalanuvchilarga xabar/reklama yuborish (Broadcast)
7. **24/7 Bepul Server (Render.com)**:
   - Kompyuter yoki noutbuk o'chiq bo'lsa ham bot serverda uzluksiz ishlayveradi.

---

## 🚀 1-Qadam: Bot Token va Admin ID olish

1. Telegramda **[@BotFather](https://t.me/BotFather)** botiga kiring va `/newbot` buyrug'i orqali yangi bot oching.
2. Berilgan **API Token**ni nusxalab oling (Masalan: `7123456789:AAF_...`).
3. O'zingizning Telegram ID raqamingizni bilish uchun **[@userinfobot](https://t.me/userinfobot)** ga kiring (Masalan: `123456789`).

---

## 💻 2-Qadam: Kompyuterda sinab ko'rish (Local Test)

1. Loyiha papkasidagi `.env` faylini oching va ma'lumotlaringizni kiriting:
   ```env
   BOT_TOKEN=bu_yerga_botfather_tokeni_yoziladi
   ADMIN_IDS=bu_yerga_sizning_telegram_id_raqamingiz
   PORT=10000
   ```
2. Terminalda botni ishga tushiring:
   ```bash
   py main.py
   ```
3. Telegramda o'z botingizga `/start` buyrug'ini yuboring va sinab ko'ring!

---

## ☁️ 3-Qadam: Render.com da 24/7 Bepul Serverga Joylash

Noutbukni o'chirib qo'ysangiz ham botingiz 24 soat to'xtovsiz ishlashi uchun uni Render.com bepul serveriga joylaymiz.

### 1. Loyihani GitHub ga yuklash:
Terminalda ushbu buyruqlarni bajaring:
```bash
git init
git add .
git commit -m "Initial commit of Telegram Game Bot"
git branch -M main
git remote add origin https://github.com/SIZNING_GITHUB_USERNAME/game-bot.git
git push -u origin main
```

### 2. Render.com da xizmat ochish:
1. **[Render.com](https://render.com/)** saytida ro'yxatdan o'ting (GitHub orqali kirish juda oson).
2. Render boshqaruv panelida **"New +"** tugmasini bosing va **"Web Service"** ni tanlang.
3. GitHub dagi `game-bot` repozitoriyangizni tanlang (**Connect**).
4. Sozlamalarni tekshiring:
   - **Name**: `telegram-game-bot`
   - **Language / Runtime**: `Python 3`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: **Free** (bepul)
5. Pastroqqa tushib **"Environment Variables"** (Muhit o'zgaruvchilari) bo'limiga kiring va 2 ta o'zgaruvchini qo'shing:
   - `BOT_TOKEN` = *Sizning BotFather tokeningiz*
   - `ADMIN_IDS` = *Sizning Telegram ID raqamingiz*
6. **"Deploy Web Service"** tugmasini bosing! 🚀
7. Bir necha daqiqada bot serverda ishga tushadi va terminalda `Bot muvaffaqiyatli ishga tushdi!` xabari chiqadi.

---

## ⏰ 4-Qadam: Render Serveri Uxlab Qolmasligi Uchun (24/7 Tirik Saqlash)

Render.com ning bepul tarifida veb-xizmatga 15 daqiqa davomida so'rov kelmasa, u uxlab qolishi mumkin. Buni oldini olish va bot 24/7 doimiy uyg'oq turishi juda oson:

1. Render da botingizning manzilini nusxalab oling (Masalan: `https://telegram-game-bot-xxxx.onrender.com`).
2. Bepul **[UptimeRobot.com](https://uptimerobot.com/)** (yoki **[cron-job.org](https://cron-job.org/)**) saytiga kiring va ro'yxatdan o'ting.
3. **"Add New Monitor"** tugmasini bosing:
   - **Monitor Type**: `HTTP(s)`
   - **Friendly Name**: `Game Bot KeepAlive`
   - **URL**: `https://telegram-game-bot-xxxx.onrender.com/health`
   - **Monitoring Interval**: `Every 5 minutes` (Har 5 daqiqada)
4. **"Create Monitor"** ni bosing.

🎉 **Bo'ldi!** Endi UptimeRobot har 5 daqiqada botingizning `/health` manziliga signal yuborib turadi. Natijada Render bepul serveri hech qachon uxlab qolmaydi va noutbukingiz o'chiq bo'lsa ham botingiz 24/7/365 uzluksiz ishlaydi!

---

## 👑 5-Qadam: Admin Panelidan Foydalanish

- Botga kiring va `/admin` buyrug'ini yozing yoki menyudagi **"👑 Admin Panel"** tugmasini bosing.
- **Yangi o'yin qo'shish**:
  1. O'yin janrini tanlang (Jangari, Poyga va hk.)
  2. O'yin nomini yozing
  3. O'yin tavsifi va hajmini yozing
  4. O'yin rasmini yuboring (yoki havolasini yozing)
  5. O'yinning APK faylini to'g'ridan-to'g'ri botga yuboring YOKI yuklab olish havolasini yozing.
- **Majburiy kanallarni ulash**:
  - Majburiy kanallar tugmasini bosing.
  - Yangi kanal qo'shishni bosing.
  - Kanal username yoki ID sini kiriting (Masalan: `@mening_kanalim`).
  - *Muhim: Botingiz a'zolarni tekshira olishi uchun ushbu kanalda administrator bo'lishi shart!*
- **Xabar tarqatish (Broadcast)**:
  - Istalgan matn, rasm yoki xabarni bir marta yuborish orqali barcha bot foydalanuvchilariga yetkazishingiz mumkin.
