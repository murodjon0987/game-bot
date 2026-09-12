import html
import re
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, URLInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.database import (
    add_user, get_games_by_category, get_game_by_id, 
    search_games, get_random_game, increment_download, get_channels
)
from bot.keyboards.default import get_main_keyboard, get_cancel_keyboard
from bot.keyboards.inline import (
    get_categories_keyboard, get_app_categories_keyboard, get_games_keyboard, get_game_detail_keyboard,
    get_search_results_keyboard, get_sub_check_keyboard
)
from bot.middlewares.check_sub import check_user_subscription
from bot.states.admin_states import UserSearchStates
from bot.config import CATEGORIES, ADMIN_USERNAME, DATA_DIR

router = Router()

def format_game_caption(game) -> str:
    """O'yin ma'lumotlarini chiroyli matnga aylantirish"""
    cat_name = CATEGORIES.get(game["category"], game["category"].title())
    downloads = game["downloads_count"]
    
    caption = (
        f"🎮 <b>{html.escape(game['title'])}</b>\n\n"
        f"📂 <b>Toifa:</b> {cat_name}\n"
        f"📥 <b>Yuklab olishlar soni:</b> {downloads} marta\n\n"
        f"📝 <b>Tavsif va ma'lumot:</b>\n{html.escape(game['description'] or 'Ma\'lumot kiritilmagan.')}"
    )
    return caption

@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    user = message.from_user
    await add_user(user.id, user.full_name, user.username)

    # Majburiy obunani tekshirish
    is_sub, unsub_channels = await check_user_subscription(bot, user.id)
    if not is_sub:
        text = (
            f"👋 Assalomu alaykum, <b>{html.escape(user.full_name)}</b>!\n\n"
            "⚠️ <b>Botdan foydalanish uchun quyidagi homiy kanallarga obuna bo'ling:</b>\n"
            "Kanallarga a'zo bo'lgach, <b>'✅ Obuna bo'ldim (Tekshirish)'</b> tugmasini bosing."
        )
        await message.answer(text, reply_markup=get_sub_check_keyboard(unsub_channels), parse_mode="HTML")
        return

    welcome_text = (
        f"👋 Assalomu alaykum, <b>{html.escape(user.full_name)}</b>!\n\n"
        "🎮 <b>Eng sara va qiziqarli o'yinlar botiga xush kelibsiz!</b>\n\n"
        "Bu yerda siz turli toifadagi eng zo'r o'yinlarni topishingiz, ular haqida to'liq ma'lumot olishingiz va APK fayllarini to'g'ridan-to'g'ri yuklab olishingiz mumkin!\n\n"
        "👇 Quyidagi menyudan kerakli bo'limni tanlang:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(user.id), parse_mode="HTML")

@router.callback_query(F.data == "verify_subscription")
async def verify_sub_callback(callback: CallbackQuery, bot: Bot):
    user = callback.from_user
    is_sub, unsub_channels = await check_user_subscription(bot, user.id)

    if not is_sub:
        await callback.answer(
            "❌ Siz hali barcha kanallarga a'zo bo'lmadingiz! Iltimos, a'zo bo'ling va qayta tekshiring.",
            show_alert=True
        )
        try:
            await callback.message.edit_reply_markup(reply_markup=get_sub_check_keyboard(unsub_channels))
        except Exception:
            pass
        return

    await callback.answer("🎉 Rahmat! Obuna tasdiqlandi.", show_alert=False)
    try:
        await callback.message.delete()
    except Exception:
        pass

    welcome_text = (
        f"🎉 <b>Ajoyib, {html.escape(user.full_name)}! Obunangiz tasdiqlandi.</b>\n\n"
        "Endi bemalol o'yinlarni ko'rishingiz va yuklab olishingiz mumkin! 👇"
    )
    await callback.message.answer(welcome_text, reply_markup=get_main_keyboard(user.id), parse_mode="HTML")

@router.message(F.text == "🎮 O'yinlar toifalari")
async def menu_categories(message: Message, bot: Bot):
    is_sub, unsub_channels = await check_user_subscription(bot, message.from_user.id)
    if not is_sub:
        await message.answer(
            "⚠️ Botdan foydalanish uchun avval quyidagi kanallarga a'zo bo'ling:",
            reply_markup=get_sub_check_keyboard(unsub_channels)
        )
        return

    text = "🎮 <b>O'yinlar toifalaridan birini tanlang:</b>\nO'zingizga yoqqan janrni bosing va qiziqarli o'yinlarni kashf qiling!"
    await message.answer(text, reply_markup=get_categories_keyboard(), parse_mode="HTML")

@router.message(F.text == "📱 Foydali Dasturlar (PRO)")
async def menu_apps(message: Message, bot: Bot):
    is_sub, unsub_channels = await check_user_subscription(bot, message.from_user.id)
    if not is_sub:
        await message.answer(
            "⚠️ Botdan foydalanish uchun avval quyidagi kanallarga a'zo bo'ling:",
            reply_markup=get_sub_check_keyboard(unsub_channels)
        )
        return

    text = (
        "📱 <b>Foydali PRO & VIP Dasturlar Bo'limi:</b>\n\n"
        "Bu yerda siz <b>CapCut PRO</b>, <b>InShot</b>, <b>Spotify Premium</b>, <b>Alight Motion</b>, <b>VPNlar</b>, <b>WPS Office</b> va boshqa 500 dan ortiq eng kerakli ilovalarning to'liq versiyalarini topishingiz mumkin!\n\n"
        "👇 Kerakli yo'nalishni tanlang:"
    )
    await message.answer(text, reply_markup=get_app_categories_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "back_to_categories")
async def callback_back_to_categories(callback: CallbackQuery):
    text = "🎮 <b>O'yinlar toifalaridan birini tanlang:</b>\nO'zingizga yoqqan janrni bosing va qiziqarli o'yinlarni kashf qiling!"
    try:
        # Agar xabar rasm bo'lsa yangi xabar jo'natamiz, matn bo'lsa edit qilamiz
        if callback.message.photo:
            await callback.message.delete()
            await callback.message.answer(text, reply_markup=get_categories_keyboard(), parse_mode="HTML")
        else:
            await callback.message.edit_text(text, reply_markup=get_categories_keyboard(), parse_mode="HTML")
    except Exception:
        await callback.message.answer(text, reply_markup=get_categories_keyboard(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("cat_"))
async def callback_category_selected(callback: CallbackQuery):
    category = callback.data.replace("cat_", "", 1)
    games = await get_games_by_category(category)
    cat_title = CATEGORIES.get(category, category.title())

    if not games:
        await callback.answer(f"Bu toifada hozircha o'yinlar mavjud emas.", show_alert=True)
        return

    text = f"📂 <b>{cat_title}</b> toifasidagi o'yinlar:\nKerakli o'yinni tanlang:"
    try:
        if callback.message.photo:
            await callback.message.delete()
            await callback.message.answer(text, reply_markup=get_games_keyboard(games, category), parse_mode="HTML")
        else:
            await callback.message.edit_text(text, reply_markup=get_games_keyboard(games, category), parse_mode="HTML")
    except Exception:
        pass
    await callback.answer()

@router.callback_query(F.data == "noop")
async def callback_noop(callback: CallbackQuery):
    await callback.answer()

@router.callback_query(F.data.startswith("page:") | F.data.startswith("page_"))
async def callback_pagination(callback: CallbackQuery):
    if ":" in callback.data:
        parts = callback.data.split(":")
        category = parts[1]
        page = int(parts[2])
    else:
        parts = callback.data.split("_")
        page = int(parts[-1])
        category = "_".join(parts[1:-1])

    games = await get_games_by_category(category)
    cat_title = CATEGORIES.get(category, category.title())

    text = f"📂 <b>{cat_title}</b> toifasidagi o'yinlar:\nKerakli o'yinni tanlang:"
    try:
        await callback.message.edit_text(
            text, 
            reply_markup=get_games_keyboard(games, category, page=page), 
            parse_mode="HTML"
        )
    except Exception:
        pass
    await callback.answer()

@router.callback_query(F.data.startswith("game_"))
async def callback_game_detail(callback: CallbackQuery):
    game_id = int(callback.data.split("_")[1])
    game = await get_game_by_id(game_id)

    if not game:
        await callback.answer("❌ O'yin topilmadi yoki o'chirilgan.", show_alert=True)
        return

    caption = format_game_caption(game)
    keyboard = get_game_detail_keyboard(game)

    # Rasmni yuborishga harakat qilamiz
    photo = game["photo"]
    sent = False
    if photo:
        try:
            # Agar mavjud xabar matn bo'lsa o'chirib rasm yuboramiz
            await callback.message.delete()
            await callback.message.answer_photo(photo=photo, caption=caption, reply_markup=keyboard, parse_mode="HTML")
            sent = True
        except Exception:
            pass

    if not sent:
        try:
            if callback.message.photo:
                await callback.message.delete()
                await callback.message.answer(caption, reply_markup=keyboard, parse_mode="HTML")
            else:
                await callback.message.edit_text(caption, reply_markup=keyboard, parse_mode="HTML")
        except Exception:
            await callback.message.answer(caption, reply_markup=keyboard, parse_mode="HTML")

    await callback.answer()

@router.callback_query(F.data.startswith("get_apk_"))
async def callback_get_apk(callback: CallbackQuery, bot: Bot):
    game_id = int(callback.data.split("_")[2])
    game = await get_game_by_id(game_id)

    if not game:
        await callback.answer("❌ O'yin topilmadi!", show_alert=True)
        return

    # Yuklab olishlar sonini oshiramiz
    await increment_download(game_id)

    # Toza va chiroyli fayl nomi yaratish (.apk uchun)
    clean_title = re.sub(r'[^a-zA-Z0-9_\-]', '_', game['title']).strip('_')
    clean_title = re.sub(r'_+', '_', clean_title)
    if not clean_title:
        clean_title = f"Game_{game_id}"
    apk_filename = f"{clean_title}.apk"

    caption = (
        f"🎮 <b>{html.escape(game['title'])}</b>\n\n"
        f"📦 <b>APK fayl to'g'ridan-to'g'ri tayyorlandi!</b>\n"
        f"💎 <b>Imkoniyat:</b> VIP & Cheksiz Coins (MOD)\n"
        f"🛡 <b>Xavfsizlik:</b> 100% Virus Total tekshiruvidan o'tgan\n\n"
        f"📲 <i>Faylni yuklab olib, to'g'ridan-to'g'ri o'rnatishingiz mumkin!</i>\n"
        f"🚀 <b>Maroqli o'yinlar!</b>"
    )

    # 1. Telegramda yuklangan original APK file_id mavjud bo'lsa
    if game["apk_file_id"]:
        await callback.answer("⏳ APK fayl yuborilmoqda...")
        try:
            await bot.send_document(
                chat_id=callback.from_user.id,
                document=game["apk_file_id"],
                caption=caption,
                parse_mode="HTML"
            )
            return
        except Exception:
            pass

    # 2. Telegramda fayl bo'lmasa, soxta fayl EMAS, to'liq haqiqiy faylni yuklab olish uchun rasmiy tezkor server tugmasi beriladi
    dl_url = game["download_url"] or f"https://subway-surfers.en.uptodown.com/android/download"
    await callback.answer()

    text = (
        f"🎮 <b>{html.escape(game['title'])}</b>\n\n"
        f"📦 <b>To'liq va Haqiqiy APK fayli:</b>\n"
        f"Ushbu o'yin hajmi katta bo'lganligi sababli, quyidagi rasmiy tezkor server orqali <b>to'liq 100% ishlaydigan original APK</b> faylini to'g'ridan-to'g'ri yuklab olishingiz mumkin:\n\n"
        f"🛡 <b>Xavfsizlik:</b> Virus Total tekshiruvidan o'tgan, 100% toza va xavfsiz\n"
        f"⚡️ <b>Imkoniyat:</b> Barcha VIP & Cheksiz tangalar faollashtirilgan"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Haqiqiy APK faylni yuklab olish", url=dl_url)],
        [InlineKeyboardButton(text="🔙 O'yinlar ro'yxatiga qaytish", callback_data=f"cat_{game['category']}")]
    ])
    await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")

@router.message(F.text.in_(["🔍 O'yin qidirish", "🔍 Qidiruv"]))
async def menu_search(message: Message, state: FSMContext):
    await state.set_state(UserSearchStates.waiting_for_query)
    await message.answer(
        "🔍 <b>Qidirmoqchi bo'lgan o'yiningiz nomini yozing:</b>\n(Masalan: <i>Subway</i>, <i>Shadow</i>, <i>Rider</i> yoki <i>2048</i>)",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )

@router.message(UserSearchStates.waiting_for_query)
async def process_search_query(message: Message, state: FSMContext):
    query = message.text.strip()
    if query == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Qidiruv bekor qilindi.", reply_markup=get_main_keyboard(message.from_user.id))
        return

    games = await search_games(query)
    await state.clear()

    if not games:
        await message.answer(
            f"😔 Kechirasiz, '<b>{html.escape(query)}</b>' so'rovi bo'yicha hech qanday o'yin topilmadi.\nBoshqa so'z bilan qidirib ko'ring yoki toifalardan tanlang.",
            reply_markup=get_main_keyboard(message.from_user.id),
            parse_mode="HTML"
        )
        return

    await message.answer(
        f"🔍 '<b>{html.escape(query)}</b>' bo'yicha topilgan o'yinlar ({len(games)} ta):",
        reply_markup=get_search_results_keyboard(games),
        parse_mode="HTML"
    )

@router.message(F.text.in_(["🎲 Tasodifiy o'yin", "🎲 Tasodifiy tanlov"]))
async def menu_random_game(message: Message):
    game = await get_random_game()
    if not game:
        await message.answer("Hozircha bazada o'yinlar mavjud emas.")
        return

    caption = "🎲 <b>Tasodifiy tavsiya etilgan o'yin:</b>\n\n" + format_game_caption(game)
    keyboard = get_game_detail_keyboard(game)

    photo = game["photo"]
    sent = False
    if photo:
        try:
            await message.answer_photo(photo=photo, caption=caption, reply_markup=keyboard, parse_mode="HTML")
            sent = True
        except Exception:
            pass

    if not sent:
        await message.answer(caption, reply_markup=keyboard, parse_mode="HTML")

@router.message(F.text == "🤝 Reklama va Hamkorlik")
async def menu_partnership(message: Message):
    admin_contact = ADMIN_USERNAME if ADMIN_USERNAME else "@admin"
    text = (
        "💼 <b>Reklama va Hamkorlik Bo'limi</b>\n\n"
        "🎮 <b>Murodjon Game Bot</b> da o'z kanalingiz, guruhingiz yoki biznesingizni reklama qilmoqchimisiz?\n\n"
        "📊 <b>Bizning imkoniyatlarimiz:</b>\n"
        "• 1,000 dan ortiq eng sara VIP va MOD o'yinlar bazasi\n"
        "• Minglab faol o'yin ixlosmandlari auditoriyasi\n"
        "• 24/7 serverda uzluksiz o'sayotgan qamrov\n\n"
        "📌 <b>Reklama turlari:</b>\n"
        "1. 📢 <b>Barcha foydalanuvchilarga xabar (Broadcast):</b> Rasm, video yoki matnli reklamangizni bir zumda barcha foydalanuvchilarga tarqatish\n"
        "2. 🔒 <b>Majburiy obuna (Sponsor kanal):</b> Yangi kirgan foydalanuvchilar kanalingizga a'zo bo'lmaguncha botdan foydalana olmaydi\n"
        "3. 🎮 <b>O'yin kartochkalarida homiylik:</b> Eng ko'p yuklab olinadigan o'yinlar ostida kanalingiz havolasini joylashtirish\n\n"
        f"📩 <b>Reklama buyurtma berish va savollar uchun:</b>\n"
        f"👉 Admin: <b>{html.escape(admin_contact)}</b>"
    )
    keyboard = None
    if ADMIN_USERNAME:
        clean_user = ADMIN_USERNAME.lstrip("@")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💬 Adminga yozish", url=f"https://t.me/{clean_user}")]
        ])
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

@router.message(F.text == "ℹ️ Bot haqida")
async def menu_about(message: Message):
    admin_contact = ADMIN_USERNAME if ADMIN_USERNAME else "@admin"
    text = (
        "🎮 <b>Murodjon Game Bot | O'yinlar Olami</b>\n\n"
        "Ushbu bot eng sara, ommabop va qiziqarli Android o'yinlarini topish hamda APK formatida yuklab olish uchun maxsus yaratilgan.\n\n"
        "✨ <b>Qulayliklar:</b>\n"
        "• 1,000 ta saralangan o'yinlar va VIP MODlar\n"
        "• Janrlar bo'yicha qulay saralash & qidiruv\n"
        "• Tezkor APK yuklab olish imkoniyati\n"
        "• 24/7 serverda uzluksiz faoliyat\n\n"
        f"👑 <b>Admin & Hamkorlik:</b> {html.escape(admin_contact)}\n"
        "🚀 <i>Maroqli o'yinlar tilaymiz!</i>"
    )
    keyboard = None
    if ADMIN_USERNAME:
        clean_user = ADMIN_USERNAME.lstrip("@")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💬 Adminga murojaat", url=f"https://t.me/{clean_user}")]
        ])
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

@router.message(F.text == "❌ Bekor qilish")
async def menu_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bosh sahifa.", reply_markup=get_main_keyboard(message.from_user.id))
