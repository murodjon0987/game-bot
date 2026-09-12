import html
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, URLInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.database import (
    add_user, get_games_by_category, get_game_by_id, 
    search_games, get_random_game, increment_download, get_channels
)
from bot.keyboards.default import get_main_keyboard, get_cancel_keyboard
from bot.keyboards.inline import (
    get_categories_keyboard, get_games_keyboard, get_game_detail_keyboard,
    get_search_results_keyboard, get_sub_check_keyboard
)
from bot.middlewares.check_sub import check_user_subscription
from bot.states.admin_states import UserSearchStates
from bot.config import CATEGORIES

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
    category = callback.data.split("_")[1]
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

@router.callback_query(F.data.startswith("page_"))
async def callback_pagination(callback: CallbackQuery):
    parts = callback.data.split("_")
    category = parts[1]
    page = int(parts[2])
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

    # 1. Telegramda saqlangan APK file_id mavjud bo'lsa
    if game["apk_file_id"]:
        await callback.answer("⏳ APK fayl yuborilmoqda...")
        caption = f"📥 <b>{html.escape(game['title'])}</b>\nO'rnatish uchun APK fayl tayyor. Marhamat!"
        try:
            await bot.send_document(
                chat_id=callback.from_user.id,
                document=game["apk_file_id"],
                caption=caption,
                parse_mode="HTML"
            )
            return
        except Exception as e:
            # Agar faylni yuborishda xatolik bo'lsa
            pass

    # 2. Agar Telegram APK bo'lmasa, web havola beriladi
    if game["download_url"]:
        await callback.answer()
        text = (
            f"📥 <b>{html.escape(game['title'])}</b>\n\n"
            "Ushbu o'yin hajmi katta bo'lganligi sababli, quyidagi tezkor rasmiy havola orqali to'g'ridan-to'g'ri APK yuklab olishingiz mumkin:\n\n"
            f"🔗 <a href='{game['download_url']}'>Yuklab olish havolasi</a>"
        )
        await callback.message.answer(text, parse_mode="HTML", disable_web_page_preview=False)
    else:
        await callback.answer("Ushbu o'yin fayli hozircha yuklanmagan.", show_alert=True)

@router.message(F.text == "🔍 O'yin qidirish")
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

@router.message(F.text == "🎲 Tasodifiy o'yin")
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

@router.message(F.text == "ℹ️ Bot haqida")
async def menu_about(message: Message):
    text = (
        "🎮 <b>O'yinlar Olami Boti</b>\n\n"
        "Ushbu bot eng sara, ommabop va qiziqarli Android o'yinlarini topish hamda APK formatida yuklab olish uchun maxsus yaratilgan.\n\n"
        "✨ <b>Qulayliklar:</b>\n"
        "• Janrlar bo'yicha qulay saralash\n"
        "• Tezkor APK yuklab olish imkoniyati\n"
        "• Doimiy yangi o'yinlar bazasi\n"
        "• 24/7 serverda uzluksiz faoliyat\n\n"
        "🚀 <i>Maroqli o'yinlar tilaymiz!</i>"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(F.text == "❌ Bekor qilish")
async def menu_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bosh sahifa.", reply_markup=get_main_keyboard(message.from_user.id))
