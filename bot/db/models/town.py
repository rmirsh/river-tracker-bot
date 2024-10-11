from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.models.base import Base


if TYPE_CHECKING:
    from bot.db.models.subscriptions_towns_association import SubscriptionTownAssociation
    from bot.db.models.subscription import Subscription


class Town(Base):
    __tablename__ = "towns"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    town: Mapped[str] = mapped_column(nullable=False)

    subscriptions: Mapped[list["Subscription"]] = relationship(
        secondary="subscriptions_towns_association",
        back_populates="towns",
        cascade="all, delete",
        overlaps="subscriptions_details,subscriptions",
    )
    subscriptions_details: Mapped[list["SubscriptionTownAssociation"]] = relationship(
        back_populates="town", overlaps="subscriptions,towns"
    )
