import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from bot.handlers import add_category_router, add_channel_router, add_site_router, category_router, profile_router, \
    start_router
from bot.handlers.organization import organ_router
from bot.utils import save_categories_to_db, save_telegram_channels_to_db, save_organizations_from_json
from config import conf
from database.base import db

logging.basicConfig(level=logging.INFO)

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(conf.bot.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
print(conf.bot.BOT_TOKEN)
current_dir = os.path.dirname(os.path.abspath(__file__))
locales_path = os.path.join(current_dir, 'locales')
i18n = I18n(path=locales_path, default_locale='uz')

dp.update.outer_middleware.register(FSMI18nMiddleware(i18n))


def setup_routers():
    dp.include_router(start_router)
    dp.include_router(category_router)
    dp.include_router(profile_router)
    dp.include_router(add_category_router)
    dp.include_router(add_channel_router)
    dp.include_router(add_site_router)
    dp.include_router(organ_router)


async def on_startup(bot: Bot):
    await db.create_all()
    await save_categories_to_db()
    await save_telegram_channels_to_db()
    await save_organizations_from_json('data.json')


async def on_shutdown(bot: Bot):
    await bot.session.close()


async def main():
    setup_routers()
    dp.startup.register(on_startup)
    # dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
