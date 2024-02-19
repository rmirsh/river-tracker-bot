from typing import TYPE_CHECKING

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base


if TYPE_CHECKING:
    from subscriptions_towns_association import SubscriptionTownAssociation
    from subscription import Subscription


class Town(Base):

    town = mapped_column(Text)

    subscriptions: Mapped[list["Subscription"]] = relationship(
        secondary="subscriptions_towns_association",
        back_populates="towns",
    )
    # association between Parent -> Association -> Child
    subscriptions_details: Mapped[list["SubscriptionTownAssociation"]] = relationship(
        back_populates="towns"
    )
