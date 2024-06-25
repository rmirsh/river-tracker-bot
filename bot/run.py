from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import asyncio
import logging
import sys

from bot.ui_commands import set_ui_commands
from bot.handlers import start, subscription
from bot.utils.csv_filler import insert_town_table_csv
from bot.utils.notifications import on_startup
from config import settings


async def main():
    """Run the main function of the program.

    This function initializes the bot, sets up the dispatcher, registers
    startup functions, includes routers, sets UI commands, deletes webhook,
    and starts polling.

    Returns:
        None.
    """

    # Delegated to alembic
    # await async_main()

    bot = Bot(
        settings.TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )
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
