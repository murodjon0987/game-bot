import html
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.config import ADMIN_IDS, CATEGORIES
from bot.database import (
    get_stats, add_game, delete_game, get_channels,
    add_channel, delete_channel, get_all_users, aiosqlite, DATABASE_PATH
)
from bot.keyboards.inline import (
    get_admin_main_keyboard, get_admin_categories_keyboard,
    get_admin_delete_games_keyboard, get_admin_channels_keyboard,
    get_admin_back_keyboard
)
from bot.keyboards.default import get_cancel_keyboard, get_main_keyboard
from bot.states.admin_states import AddGameStates, AddChannelStates, BroadcastStates

router = Router()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@router.message(Command("admin"))
@router.message(F.text == "👑 Admin Panel")
async def cmd_admin_panel(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Ushbu bo'lim faqat bot administratorlari uchun ochiq!")
        return

    await state.clear()
    text = (
        "👑 <b>Admin Boshqaruv Paneli</b>\n\n"
        "Xush kelibsiz, administrator! Quyidagi tugmalar orqali botni to'liq boshqarishingiz mumkin:"
    )
    await message.answer(text, reply_markup=get_admin_main_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "adm_back")
async def callback_admin_back(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return
    await state.clear()
    text = (
        "👑 <b>Admin Boshqaruv Paneli</b>\n\n"
        "Quyidagi tugmalar orqali botni boshqarishingiz mumkin:"
    )
    try:
        await callback.message.edit_text(text, reply_markup=get_admin_main_keyboard(), parse_mode="HTML")
    except Exception:
        await callback.message.answer(text, reply_markup=get_admin_main_keyboard(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "adm_cancel")
async def callback_admin_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    text = "Amal bekor qilindi. Boshqaruv paneliga qaytildi."
    try:
        await callback.message.edit_text(text, reply_markup=get_admin_main_keyboard(), parse_mode="HTML")
    except Exception:
        await callback.message.answer(text, reply_markup=get_admin_main_keyboard(), parse_mode="HTML")
    await callback.answer()

# ==================== STATISTIKA ====================

@router.callback_query(F.data == "adm_stats")
async def callback_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    stats = await get_stats()
    text = (
        "📊 <b>Bot Statistikasi:</b>\n\n"
        f"👥 <b>Jami foydalanuvchilar:</b> {stats['total_users']} ta\n"
        f"🎮 <b>Bazada mavjud o'yinlar:</b> {stats['total_games']} ta\n"
        f"📥 <b>Jami yuklab olishlar:</b> {stats['total_downloads']} marta\n"
        f"📢 <b>Faol majburiy kanallar:</b> {stats['total_channels']} ta\n"
    )
    await callback.message.edit_text(text, reply_markup=get_admin_back_keyboard(), parse_mode="HTML")
    await callback.answer()

# ==================== YANGI O'YIN QO'SHISH ====================

@router.callback_query(F.data == "adm_add_game")
async def callback_add_game_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await state.set_state(AddGameStates.waiting_for_category)
    text = "➕ <b>1/5. Yangi o'yin toifasini (janrini) tanlang:</b>"
    await callback.message.edit_text(text, reply_markup=get_admin_categories_keyboard(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(AddGameStates.waiting_for_category, F.data.startswith("adm_cat_"))
async def process_game_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.replace("adm_cat_", "")
    await state.update_data(category=category)
    await state.set_state(AddGameStates.waiting_for_title)
    
    cat_title = CATEGORIES.get(category, category)
    text = (
        f"✅ Toifa tanlandi: <b>{cat_title}</b>\n\n"
        "🎮 <b>2/5. O'yin nomini yozing:</b>\n"
        "(Masalan: <i>PUBG Mobile</i> yoki <i>Need for Speed</i>)"
    )
    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()

@router.message(AddGameStates.waiting_for_title)
async def process_game_title(message: Message, state: FSMContext):
    title = message.text.strip()
    if title == "❌ Bekor qilish":
        await state.clear()
        await message.answer("O'yin qo'shish bekor qilindi.", reply_markup=get_main_keyboard(message.from_user.id))
        return

    await state.update_data(title=title)
    await state.set_state(AddGameStates.waiting_for_description)
    text = (
        f"✅ O'yin nomi: <b>{html.escape(title)}</b>\n\n"
        "📝 <b>3/5. O'yin tavsifi va ma'lumotlarini kiriting:</b>\n"
        "(O'yin haqida qisqacha ma'lumot, hajmi, versiyasi yoki MOD xususiyatlari)"
    )
    await message.answer(text, reply_markup=get_cancel_keyboard(), parse_mode="HTML")

@router.message(AddGameStates.waiting_for_description)
async def process_game_description(message: Message, state: FSMContext):
    desc = message.text.strip()
    if desc == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=get_main_keyboard(message.from_user.id))
        return

    await state.update_data(description=desc)
    await state.set_state(AddGameStates.waiting_for_photo)
    text = (
        "🖼 <b>4/5. O'yin uchun rasm (banner) yuboring:</b>\n\n"
        "• Botga rasm faylini yuborishingiz\n"
        "• Yoki rasm URL havolasini yozishingiz mumkin.\n"
        "• Rasm qo'shmaslik uchun <code>/skip</code> deb yozing."
    )
    await message.answer(text, reply_markup=get_cancel_keyboard(), parse_mode="HTML")

@router.message(AddGameStates.waiting_for_photo)
async def process_game_photo(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=get_main_keyboard(message.from_user.id))
        return

    photo_id = None
    if message.photo:
        # Telegram rasm file_id
        photo_id = message.photo[-1].file_id
    elif message.text and (message.text.startswith("http://") or message.text.startswith("https://")):
        photo_id = message.text.strip()
    elif message.text and message.text == "/skip":
        photo_id = None
    else:
        await message.answer("Iltimos, rasm yuboring, rasm havolasini yozing yoki /skip deb yozing.")
        return

    await state.update_data(photo=photo_id)
    await state.set_state(AddGameStates.waiting_for_file_or_link)

    text = (
        "📥 <b>5/5. O'yin fayli yoki havolasini kiriting:</b>\n\n"
        "Quyidagilardan birini amalga oshiring:\n"
        "1. <b>APK faylini</b> botga to'g'ridan-to'g'ri hujjat (document) sifatida tashlang\n"
        "2. YOKI to'g'ridan-to'g'ri <b>yuklab olish havolasini (URL)</b> matn qilib yuboring."
    )
    await message.answer(text, reply_markup=get_cancel_keyboard(), parse_mode="HTML")

@router.message(AddGameStates.waiting_for_file_or_link)
async def process_game_file_or_link(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=get_main_keyboard(message.from_user.id))
        return

    data = await state.get_data()
    apk_file_id = None
    download_url = None

    if message.document:
        apk_file_id = message.document.file_id
    elif message.text:
        download_url = message.text.strip()
    else:
        await message.answer("Iltimos, APK faylini yuboring yoki yuklab olish havolasini yozing.")
        return

    await add_game(
        category=data["category"],
        title=data["title"],
        description=data["description"],
        photo=data["photo"],
        apk_file_id=apk_file_id,
        download_url=download_url
    )
    await state.clear()

    success_text = (
        f"🎉 <b>O'yin muvaffaqiyatli qo'shildi!</b>\n\n"
        f"🎮 Nomi: <b>{html.escape(data['title'])}</b>\n"
        f"📂 Toifa: {CATEGORIES.get(data['category'], data['category'])}\n"
        f"📦 Fayl/Havola: {'Telegram APK yuklandi ✅' if apk_file_id else 'Web Havola ✅'}"
    )
    await message.answer(success_text, reply_markup=get_main_keyboard(message.from_user.id), parse_mode="HTML")

# ==================== O'YINNI O'CHIRISH ====================

@router.callback_query(F.data == "adm_del_game")
async def callback_delete_game_list(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return

    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT id, title FROM games ORDER BY id DESC LIMIT 30")
        games = await cur.fetchall()

    if not games:
        await callback.message.edit_text("Bazada o'yinlar mavjud emas.", reply_markup=get_admin_back_keyboard())
        return

    text = "🗑 <b>O'chirmoqchi bo'lgan o'yiningizni tanlang:</b>"
    await callback.message.edit_text(text, reply_markup=get_admin_delete_games_keyboard(games), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("adm_rmgame_"))
async def callback_delete_game_confirm(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    game_id = int(callback.data.split("_")[2])
    await delete_game(game_id)
    await callback.answer("✅ O'yin muvaffaqiyatli o'chirildi!", show_alert=True)
    await callback_delete_game_list(callback)

# ==================== MAJBURIY KANALLAR BOSHQARUVI ====================

@router.callback_query(F.data == "adm_channels")
async def callback_channels_list(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    channels = await get_channels()
    text = (
        "📢 <b>Majburiy obuna kanallari boshqaruvi</b>\n\n"
        "Foydalanuvchilar botga kirganda shu kanallarga a'zo bo'lishi shart bo'ladi.\n"
        "<i>Eslatma: Bot ushbu kanallarda administrator bo'lishi kerak!</i>"
    )
    await callback.message.edit_text(text, reply_markup=get_admin_channels_keyboard(channels), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "adm_add_channel")
async def callback_add_channel_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await state.set_state(AddChannelStates.waiting_for_chat_id)
    text = (
        "📢 <b>1/3. Kanal username yoki ID sini yuboring:</b>\n\n"
        "Masalan: <code>@kanal_username</code> yoki <code>-1001234567890</code>\n"
        "<i>(Bot ushbu kanalda administrator bo'lishi shart)</i>"
    )
    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()

@router.message(AddChannelStates.waiting_for_chat_id)
async def process_channel_chat_id(message: Message, state: FSMContext):
    chat_id = message.text.strip()
    if chat_id == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=get_main_keyboard(message.from_user.id))
        return

    await state.update_data(chat_id=chat_id)
    await state.set_state(AddChannelStates.waiting_for_title)
    await message.answer(
        "📝 <b>2/3. Kanal nomini yozing (Tugmada aks etadi):</b>\n(Masalan: <i>Bizning rasmiy kanal</i>)",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )

@router.message(AddChannelStates.waiting_for_title)
async def process_channel_title(message: Message, state: FSMContext):
    title = message.text.strip()
    if title == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=get_main_keyboard(message.from_user.id))
        return

    await state.update_data(title=title)
    await state.set_state(AddChannelStates.waiting_for_invite_link)
    await message.answer(
        "🔗 <b>3/3. Kanalga kirish havolasini yuboring:</b>\n(Masalan: <i>https://t.me/kanal_username</i>)",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )

@router.message(AddChannelStates.waiting_for_invite_link)
async def process_channel_invite_link(message: Message, state: FSMContext):
    link = message.text.strip()
    if link == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=get_main_keyboard(message.from_user.id))
        return

    data = await state.get_data()
    await add_channel(chat_id=data["chat_id"], title=data["title"], invite_link=link)
    await state.clear()

    await message.answer(
        f"✅ <b>Kanal muvaffaqiyatli qo'shildi!</b>\n\n"
        f"📢 Nomi: {html.escape(data['title'])}\n"
        f"🆔 Chat ID: {html.escape(data['chat_id'])}\n"
        f"🔗 Havola: {html.escape(link)}",
        reply_markup=get_main_keyboard(message.from_user.id),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("adm_rmchannel_"))
async def callback_delete_channel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    channel_id = int(callback.data.split("_")[2])
    await delete_channel(channel_id)
    await callback.answer("✅ Kanal o'chirildi!", show_alert=True)
    await callback_channels_list(callback)

# ==================== XABAR TARQATISH (BROADCAST) ====================

@router.callback_query(F.data == "adm_broadcast")
async def callback_broadcast_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await state.set_state(BroadcastStates.waiting_for_message)
    text = (
        "✉️ <b>Barcha foydalanuvchilarga xabar yuborish</b>\n\n"
        "Yubormoqchi bo'lgan xabaringizni (matn, rasm yoki post) yuboring.\n"
        "Bekor qilish uchun '❌ Bekor qilish' deb yozing."
    )
    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()

@router.message(BroadcastStates.waiting_for_message)
async def process_broadcast_message(message: Message, state: FSMContext, bot: Bot):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Xabar tarqatish bekor qilindi.", reply_markup=get_main_keyboard(message.from_user.id))
        return

    await state.clear()
    users = await get_all_users()
    total = len(users)

    if total == 0:
        await message.answer("Bazada hech qanday foydalanuvchi yo'q.")
        return

    status_msg = await message.answer(f"⏳ Xabar tarqatish boshlandi... Jami: {total} ta foydalanuvchi.")
    success = 0
    failed = 0

    for user_id in users:
        try:
            await message.copy_to(chat_id=user_id)
            success += 1
            await asyncio.sleep(0.05) # Telegram spam chegarasi (flood control)
        except Exception:
            failed += 1

    await status_msg.edit_text(
        f"✅ <b>Xabar tarqatish yakunlandi!</b>\n\n"
        f"📤 Yuborildi: {success} ta\n"
        f"❌ Yetib bormadi (bloklagan): {failed} ta\n"
        f"👥 Jami: {total} ta",
        parse_mode="HTML"
    )
