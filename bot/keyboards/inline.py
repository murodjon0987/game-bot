from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import CATEGORIES

def get_categories_keyboard() -> InlineKeyboardMarkup:
    """O'yin toifalari (kategoriyalar) tugmalari"""
    buttons = []
    cat_items = list(CATEGORIES.items())
    
    # 2 tadan qatorlarga ajratish
    for i in range(0, len(cat_items), 2):
        row = []
        key1, name1 = cat_items[i]
        row.append(InlineKeyboardButton(text=name1, callback_data=f"cat_{key1}"))
        if i + 1 < len(cat_items):
            key2, name2 = cat_items[i + 1]
            row.append(InlineKeyboardButton(text=name2, callback_data=f"cat_{key2}"))
        buttons.append(row)
        
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_games_keyboard(games, category: str, page: int = 1, per_page: int = 8) -> InlineKeyboardMarkup:
    """Muayyan toifadagi o'yinlar ro'yxati tugmalari (sahifalash / pagination bilan)"""
    total_games = len(games)
    total_pages = max(1, (total_games + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    current_games = games[start_idx:end_idx]
    
    buttons = []
    for game in current_games:
        downloads = f"({game['downloads_count']} ⬇️)" if game['downloads_count'] > 0 else ""
        text = f"🎮 {game['title']} {downloads}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"game_{game['id']}")])
        
    # Sahifalash navigatsiyasi (agar o'yinlar 1 sahifadan ko'p bo'lsa)
    if total_pages > 1:
        nav_row = []
        if page > 1:
            nav_row.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"page_{category}_{page - 1}"))
        nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop"))
        if page < total_pages:
            nav_row.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"page_{category}_{page + 1}"))
        buttons.append(nav_row)
        
    # Orqaga qaytish tugmasi
    buttons.append([InlineKeyboardButton(text="🔙 Toifalarga qaytish", callback_data="back_to_categories")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_game_detail_keyboard(game) -> InlineKeyboardMarkup:
    """O'yin tafsilotlari va yuklab olish tugmalari"""
    buttons = []
    
    # 1. Haqiqiy va to'liq APK yuklab olish (Rasmiy tezkor server)
    dl_url = game["download_url"] or f"https://subway-surfers.en.uptodown.com/android/download"
    buttons.append([
        InlineKeyboardButton(
            text="🚀 Haqiqiy APK yuklab olish (Rasmiy Server)", 
            url=dl_url
        )
    ])
    
    # 2. Telegram orqali yuklash varianti
    buttons.append([
        InlineKeyboardButton(
            text="📥 Telegram orqali olish (APK)", 
            callback_data=f"get_apk_{game['id']}"
        )
    ])
    
    # 3. Orqaga qaytish tugmasi
    buttons.append([
        InlineKeyboardButton(
            text="🔙 O'yinlar ro'yxatiga qaytish", 
            callback_data=f"cat_{game['category']}"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_search_results_keyboard(games) -> InlineKeyboardMarkup:
    """Qidiruv natijalari tugmalari (birinchi 10 ta)"""
    buttons = []
    for game in games[:10]:
        buttons.append([
            InlineKeyboardButton(
                text=f"🎮 {game['title']}", 
                callback_data=f"game_{game['id']}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 Asosiy toifalar", callback_data="back_to_categories")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_sub_check_keyboard(channels) -> InlineKeyboardMarkup:
    """Majburiy obuna kanallari va tekshirish tugmasi"""
    buttons = []
    for ch in channels:
        buttons.append([
            InlineKeyboardButton(
                text=f"📢 {ch['title']}", 
                url=ch["invite_link"]
            )
        ])
        
    buttons.append([
        InlineKeyboardButton(
            text="✅ Obuna bo'ldim (Tekshirish)", 
            callback_data="verify_subscription"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ==================== ADMIN KEYBOARDS ====================

def get_admin_main_keyboard() -> InlineKeyboardMarkup:
    """Admin boshqaruv paneli tugmalari"""
    buttons = [
        [
            InlineKeyboardButton(text="➕ Yangi o'yin qo'shish", callback_data="adm_add_game"),
            InlineKeyboardButton(text="🗑 O'yinni o'chirish", callback_data="adm_del_game")
        ],
        [
            InlineKeyboardButton(text="📢 Majburiy kanallar", callback_data="adm_channels"),
            InlineKeyboardButton(text="📊 Statistika", callback_data="adm_stats")
        ],
        [
            InlineKeyboardButton(text="✉️ Xabar tarqatish (Broadcast)", callback_data="adm_broadcast")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_categories_keyboard() -> InlineKeyboardMarkup:
    """O'yin qo'shishda kategoriya tanlash"""
    buttons = []
    for key, name in CATEGORIES.items():
        buttons.append([InlineKeyboardButton(text=name, callback_data=f"adm_cat_{key}")])
    buttons.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data="adm_cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_delete_games_keyboard(games) -> InlineKeyboardMarkup:
    """O'yinni o'chirish ro'yxati"""
    buttons = []
    for g in games:
        buttons.append([InlineKeyboardButton(text=f"❌ {g['title']}", callback_data=f"adm_rmgame_{g['id']}")])
    buttons.append([InlineKeyboardButton(text="🔙 Admin menyu", callback_data="adm_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_channels_keyboard(channels) -> InlineKeyboardMarkup:
    """Kanallar boshqaruvi tugmalari"""
    buttons = [
        [InlineKeyboardButton(text="➕ Yangi kanal qo'shish", callback_data="adm_add_channel")]
    ]
    for ch in channels:
        buttons.append([
            InlineKeyboardButton(
                text=f"❌ O'chirish: {ch['title']}", 
                callback_data=f"adm_rmchannel_{ch['id']}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 Admin menyu", callback_data="adm_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_back_keyboard() -> InlineKeyboardMarkup:
    """Orqaga admin menyuga qaytish"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Admin menyuga qaytish", callback_data="adm_back")]
    ])
