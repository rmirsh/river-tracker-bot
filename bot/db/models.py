import os
from typing import List

from sqlalchemy import BigInteger, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import dotenv


dotenv.load_dotenv()

engine = create_async_engine(os.getenv("SQLALCHEMY_ENGINE"), echo=True)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Town(Base):
    __tablename__ = 'towns'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    town = mapped_column(Text)


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger, nullable=False)
    is_subscribed: Mapped[bool] = mapped_column(default=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
