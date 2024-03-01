import asyncio
import csv

from sqlalchemy import select

from bot.db import Town
from bot.db.make_models import async_session


async def fill_town_table_csv():
    with open("towns_data.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)

        async with async_session() as session:
            for row in reader:
                record_exist = await session.scalar(
                    select(Town.town).where(Town.town == row["town_name"])
                )
                if not record_exist:
                    session.add(Town(town=row["town_name"]))

                await session.commit()


asyncio.run(fill_town_table_csv())
