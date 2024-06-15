import asyncio

from aiogram import Bot

from emercit_parse.async_emercit_data import a_get_river_data, towns


async def send_warning(bot: Bot):
    while True:
        for town in towns:
            river_data = await a_get_river_data(town)
            if river_data.current_river_level < river_data.prevention_level:
                await bot.send_message(446913605, f"{town}")
                await asyncio.sleep(2)


async def on_startup(bot: Bot):
    asyncio.create_task(send_warning(bot))
