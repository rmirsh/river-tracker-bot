from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger

from .base import Base

if TYPE_CHECKING:
    from .subscriptions_towns_association import SubscriptionTownAssociation
    from .town import Town


class Subscription(Base):
    __tablename__ = "subscriptions"
    # __table_args__ = {"extend_existing": True}

    telegram_id = mapped_column(BigInteger, nullable=False)
    chat_id = mapped_column(BigInteger, nullable=False)
    is_subscribed: Mapped[bool] = mapped_column(nullable=False)

    towns: Mapped[list["Town"]] = relationship(
        secondary="subscriptions_towns_association",
        back_populates="subscriptions",
        cascade="all, delete",
        overlaps="towns_details,subscriptions",
    )
    towns_details: Mapped[list["SubscriptionTownAssociation"]] = relationship(
        back_populates="subscription", overlaps="towns,subscriptions"
    )
