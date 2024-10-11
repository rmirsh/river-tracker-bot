from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db import Base


if TYPE_CHECKING:
    from town import Town
    from bot.db.models.subscription import Subscription


class SubscriptionTownAssociation(Base):
    __tablename__ = "subscriptions_towns_association"
    __table_args__ = (
        UniqueConstraint(
            "subscription_id",
            "town_id",
            name="idx_unique_subscription_town",
        ),
        # {"extend_existing": True},
    )

    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("subscriptions.id"), primary_key=True
    )
    town_id: Mapped[int] = mapped_column(ForeignKey("towns.id"), primary_key=True)

    subscription: Mapped["Subscription"] = relationship(
        back_populates="towns_details", overlaps="subscriptions,towns"
    )
    town: Mapped["Town"] = relationship(
        back_populates="subscriptions_details", overlaps="subscriptions,towns"
    )
