from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.config import ADMIN_IDS

def get_main_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Asosiy menyu tugmalari"""
    buttons = [
        [
            KeyboardButton(text="🎮 O'yinlar toifalari"),
            KeyboardButton(text="📱 Foydali Dasturlar (PRO)")
        ],
        [
            KeyboardButton(text="🔍 Qidiruv"),
            KeyboardButton(text="🎲 Tasodifiy tanlov")
        ],
        [
            KeyboardButton(text="🤝 Reklama va Hamkorlik"),
            KeyboardButton(text="ℹ️ Bot haqida")
        ]
    ]
    
    # Agar foydalanuvchi admin bo'lsa, Admin paneli tugmasi qo'shiladi
    if user_id in ADMIN_IDS:
        buttons.append([KeyboardButton(text="👑 Admin Panel")])
        
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Quyidagi bo'limlardan birini tanlang..."
    )

def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Amalni bekor qilish tugmasi"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True
    )
