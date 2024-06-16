import asyncio

from aiogram import Bot

from bot.db.requests import get_subs_chat_id
from emercit_parse.async_emercit_data import async_get_river_data, towns


async def send_warning(bot: Bot) -> None:
    while True:
        for town in towns:
            river_data = await async_get_river_data(town)
            if river_data.current_river_level < river_data.prevention_level:
                subs_id = await get_subs_chat_id()
                subs_id_integers = convert_nested_list_to_integers(subs_id)
                for sub_id in subs_id_integers:
                    await bot.send_message(sub_id, f"{town}")
                    await asyncio.sleep(2)


def convert_nested_list_to_integers(nested_list: list[list[str]]) -> list[int]:
    list_of_integers = [int(string) for row in nested_list for string in row]

    return list_of_integers


async def on_startup(bot: Bot):
    asyncio.create_task(send_warning(bot))
