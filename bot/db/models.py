import os

from sqlalchemy import BigInteger, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import dotenv


dotenv.load_dotenv()

engine = create_async_engine(os.getenv("SQLALCHEMY_ENGINE"), echo=True)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Subscription(Base):
    __tablename__ = 'subscriptions'

    # id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BigInteger, primary_key=True)
    is_subscribed: Mapped[bool] = mapped_column(Boolean)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
