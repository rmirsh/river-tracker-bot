from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base


if TYPE_CHECKING:
    from subscriptions_towns_association import SubscriptionTownAssociation
    from subscription import Subscription


class Town(Base):

    town: Mapped[str] = mapped_column()

    subscriptions: Mapped[list["Subscription"]] = relationship(
        secondary="subscriptions_towns_association",
        back_populates="towns",
        cascade="all, delete",
    )
    # association between Parent -> Association -> Child
    subscriptions_details: Mapped[list["SubscriptionTownAssociation"]] = relationship(
        back_populates="town"
    )
