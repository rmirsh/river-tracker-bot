from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger

from .base import Base

if TYPE_CHECKING:
    from .subscriptions_towns_association import SubscriptionTownAssociation
    from .town import Town


class Subscription(Base):

    telegram_id = mapped_column(BigInteger, nullable=False)
    is_subscribed: Mapped[bool] = mapped_column(default=False)

    towns: Mapped[list["Town"]] = relationship(
        secondary="subscriptions_towns_association",
        back_populates="subscriptions",
    )
    # association between Parent -> Association -> Child
    towns_details: Mapped[list["SubscriptionTownAssociation"]] = relationship(
        back_populates="subscription"
    )
