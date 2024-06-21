import asyncio
import csv
import os

from sqlalchemy import select

from bot.db import Town
from bot.db.make_models import async_session


async def insert_town_table_csv():
    """Insert town data from a CSV file into the database.

    Reads the data from the specified CSV file containing town information.
    For each row in the CSV, it checks if the town already exists in the
    database. If not, it adds the town to the database.
    """

    with open("/app/bot/utils/towns_data.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)

        async with async_session() as session:
            for row in reader:
                record_exist = await session.scalar(
                    select(Town.town).where(Town.town == row["town_name"])
                )
                if not record_exist:
                    session.add(Town(town=row["town_name"]))

                await session.commit()
