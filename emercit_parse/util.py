import asyncio

from emercit_data import get_river_data


async def send_data_loop(seconds: int = 10, n: int = 3):
    while n:
        n -= 1
        await asyncio.sleep(seconds)
        return get_river_data("Горячий Ключ")
