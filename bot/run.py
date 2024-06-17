from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

import asyncio
import logging
import sys
import warnings

from bot.ui_commands import set_ui_commands
from bot.handlers import start, subscription
from bot.db.make_models import async_main
from bot.utils.csv_filler import insert_town_table_csv
from bot.utils.notifications import on_startup
from config import settings


async def main():
    await async_main()

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    bot = Bot(settings.TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.startup.register(insert_town_table_csv)
    dp.include_routers(start.router, subscription.router)

    await set_ui_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
