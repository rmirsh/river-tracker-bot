from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db import Base


if TYPE_CHECKING:
    from town import Town
    from subscription import Subscription


class SubscriptionTownAssociation(Base):
    __tablename__ = "subscriptions_towns_association"
    __table_args__ = (
        UniqueConstraint(
            "subscription_id",
            "town_id",
            name="idx_unique_subscription_town",
        ),
    )

    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"))
    town_id: Mapped[int] = mapped_column(ForeignKey("towns.id"))

    # association between Association -> Subscription
    subscription: Mapped["Subscription"] = relationship(
        back_populates="towns_details",
    )
    # association between Association -> Town
    town: Mapped["Town"] = relationship(
        back_populates="subscriptions_details",
    )
