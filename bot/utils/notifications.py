import asyncio

from aiogram import Bot

from bot.db.crud.requests import get_subs_chat_id_and_town
from config import settings
from parser import river_parser


async def send_warning(bot: Bot) -> None:
    """Continuously checks river data for each town and sends warning messages
    if necessary.

    Args:
        bot (Bot): The bot instance used to send messages.
    """

    while True:
        subs_id_town = await get_subs_chat_id_and_town()
        for row in subs_id_town:
            chat_id, town = row
            river_data = await river_parser.fetch_river_data(town)
            if river_data.current_river_level >= river_data.prevention_level:
                await bot.send_message(
                    chat_id,
                    f"<b>❗️УГРОЗА❗️\n</b>Возможно затопление в населённом пункте {town}.\n"
                    f"Текущий уровень воды - <b>{river_data.current_river_level} м</b>",
                )
            elif river_data.current_river_level >= river_data.danger_level:
                await bot.send_message(
                    chat_id,
                    f"<u><b>‼️️ОПАСНОСТЬ‼️</b></u>\nУровень воды в населённом пункте {town} поднялся о опасных значений.\n"
                    f"Текущий уровень воды - <b>{river_data.current_river_level} м</b>",
                )
        await asyncio.sleep(settings.parser.delay)


async def on_startup(bot: Bot):
    """Perform tasks when the bot starts up.

    This function creates a new asynchronous task to send a warning message
    using the provided bot instance.

    Args:
        bot (Bot): The bot instance that triggers the startup.
    """

    asyncio.create_task(send_warning(bot))
