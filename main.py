import asyncio
import logging
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import BOT_TOKEN, PORT
from bot.database import init_db
from bot.handlers import user, admin

# Windows console UTF-8 qo'llab-quvvatlash
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("GameBot")

async def health_check(request):
    """Render.com uchun HTTP health-check endpointi (24/7 server faolligi)"""
    return web.json_response({
        "status": "ok",
        "service": "Telegram Game Bot",
        "message": "Bot muvaffaqiyatli ishlamoqda!"
    })

async def create_web_app():
    """aiohttp web ilovasini yaratish"""
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    return app

async def main():
    # 1. Ma'lumotlar bazasini initsializatsiya qilish
    logger.info("Ma'lumotlar bazasi initsializatsiya qilinmoqda...")
    await init_db()
    logger.info("Ma'lumotlar bazasi tayyor!")

    # 2. Web serverni Render.com portida ishga tushirish
    app = await create_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"🌐 Web server 0.0.0.0:{PORT} portida ishga tushdi (Render.com 24/7 rejim uchun tayyor).")

    # 3. Token tekshiruvi
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or "YOUR" in BOT_TOKEN:
        logger.warning("=" * 60)
        logger.warning("⚠️ DIQQAT: BOT_TOKEN o'rnatilmagan yoki namuna holatida turibdi!")
        logger.warning("Iltimos, .env fayliga BotFather dan olgan haqiqiy tokeningizni yozing.")
        logger.warning("Web server ishlashda davom etadi...")
        logger.warning("=" * 60)
        # Server o'chib qolmasligi uchun kutib turadi
        while True:
            await asyncio.sleep(3600)

    # 4. Bot va Dispatcherni ishga tushirish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(admin.router)
    dp.include_router(user.router)

    bot_info = await bot.get_me()
    logger.info(f"🤖 Bot muvaffaqiyatli ishga tushdi: @{bot_info.username} (ID: {bot_info.id})")

    try:
        # Eski kutilayotgan yangilanishlarni o'chirish va pollingni boshlash
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        logger.info("Bot to'xtatilmoqda...")
        await bot.session.close()
        await runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
