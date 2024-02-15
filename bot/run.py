from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import dotenv

import asyncio
import logging
import sys
import os

from bot.ui_commands import set_ui_commands
from bot.handlers import main_router, subscription
from bot.db.models import async_main


dotenv.load_dotenv('../.env')
TOKEN = os.getenv('TOKEN')


async def main():
    await async_main()

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(main_router.router, subscription.router)

    await set_ui_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
