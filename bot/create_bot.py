from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.core.bot_commands import set_ui_commands
from bot.handlers import start, subscription, donate
from bot.utils.csv_filler import insert_towns_from_csv
from bot.utils.notifications import on_startup
from config import settings


async def setup_bot(delete_webhooks: bool = True):
    """Create and return a bot instance.

    This function initializes the bot with the appropriate token and default
    properties. Sets up UI commands and returns the bot instance.

    Returns:
        bot (Bot): The initialized bot instance.
    """
    bot = Bot(
        token=settings.bot.token if settings.general.is_prod else settings.bot.test_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )
    await set_ui_commands(bot)
    await bot.delete_webhook(drop_pending_updates=delete_webhooks)

    return bot


async def setup_dispather():
    """Run the main function of the program.

    This function sets up the dispatcher, registers
    startup functions, includes router.

    Returns:
        dp (Dispatcher): The initialized dispatcher instance.
    """
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.startup.register(insert_towns_from_csv)
    dp.include_routers(
        start.router,
        subscription.router,
        donate.router,
    )

    return dp
