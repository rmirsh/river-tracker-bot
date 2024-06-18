from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.db import Base
from config import settings


engine = create_async_engine(settings.DB_URL, echo=False)
async_session = async_sessionmaker(engine)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
