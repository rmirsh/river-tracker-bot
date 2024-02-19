from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.db.base import Base
from config import settings


engine = create_async_engine(settings.DB_URL, echo=True)
async_session = async_sessionmaker(engine)


if TYPE_CHECKING:
    from subscriptions_towns_association import SubscriptionTownAssociation


class Town(Base):
    __tablename__ = "towns"

    town = mapped_column(Text)

    subscriptions: Mapped[list["Subscription"]] = relationship(
        secondary="subscriptions_towns_association",
        back_populates="towns",
    )
    # association between Parent -> Association -> Child
    subscriptions_details: Mapped[list["SubscriptionTownAssociation"]] = relationship(
        back_populates="towns"
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    telegram_id = mapped_column(BigInteger, nullable=False)
    is_subscribed: Mapped[bool] = mapped_column(default=False)

    towns: Mapped[list["Town"]] = relationship(
        secondary="subscriptions_towns_association",
        back_populates="subscriptions",
    )
    # association between Parent -> Association -> Child
    towns_details: Mapped[list["SubscriptionTownAssociation"]] = relationship(
        back_populates="subscriptions"
    )


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
