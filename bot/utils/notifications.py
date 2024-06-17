import asyncio

from aiogram import Bot

from bot.db.requests import get_subs_chat_id_and_town
from emercit_parse.async_emercit_data import async_get_river_data


async def send_warning(bot: Bot) -> None:
    while True:
        subs_id_town = await get_subs_chat_id_and_town()
        for row in subs_id_town:
            chat_id, town = row
            river_data = await async_get_river_data(town)
            # if True:
            if river_data.current_river_level >= river_data.prevention_level:
                await bot.send_message(
                    chat_id,
                    f"Возможно затопление в населённом пункте {town}.\n"
                    f"Текущий уровень воды - {river_data.current_river_level}",
                )
            elif river_data.current_river_level >= river_data.danger_level:
                await bot.send_message(
                    chat_id,
                    f"Уровень воды поднялся до опасных значений.\n"
                    f"Текущий уровень воды - {river_data.current_river_level}",
                )
        await asyncio.sleep(60*30)


async def on_startup(bot: Bot):
    asyncio.create_task(send_warning(bot))
