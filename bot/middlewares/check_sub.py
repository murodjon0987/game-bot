import logging
from aiogram import Bot
from bot.database import get_channels
from bot.config import ADMIN_IDS

logger = logging.getLogger(__name__)

async def check_user_subscription(bot: Bot, user_id: int):
    """
    Foydalanuvchi majburiy kanallarga a'zo bo'lganini tekshirish.
    Adminlar uchun avtomatik ruxsat beriladi.
    Qaytaradi: (bool is_subscribed, list unsubscribed_channels)
    """
    if user_id in ADMIN_IDS:
        return True, []

    channels = await get_channels()
    if not channels:
        return True, []

    unsubscribed = []

    for channel in channels:
        chat_id = channel["chat_id"]
        try:
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status in ["left", "kicked"]:
                unsubscribed.append(channel)
        except Exception as e:
            # Agar bot kanalda admin bo'lmasa yoki kanal topilmasa, bot qotib qolmasligi uchun log qilib o'tkazib yuboramiz
            logger.warning(f"Kanalga a'zolikni tekshirib bo'lmadi ({chat_id}): {e}")
            continue

    is_subscribed = len(unsubscribed) == 0
    return is_subscribed, unsubscribed
