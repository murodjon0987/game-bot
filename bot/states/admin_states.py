from aiogram.fsm.state import State, StatesGroup

class AddGameStates(StatesGroup):
    """Yangi o'yin qo'shish qadamlari"""
    waiting_for_category = State()
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_photo = State()
    waiting_for_file_or_link = State()

class AddChannelStates(StatesGroup):
    """Yangi majburiy kanal qo'shish qadamlari"""
    waiting_for_chat_id = State()
    waiting_for_title = State()
    waiting_for_invite_link = State()

class BroadcastStates(StatesGroup):
    """Barcha foydalanuvchilarga xabar tarqatish"""
    waiting_for_message = State()

class UserSearchStates(StatesGroup):
    """Foydalanuvchi qidiruv holati"""
    waiting_for_query = State()
