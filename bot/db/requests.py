from bot.db import SubscriptionTownAssociation
from bot.db.town import Town
from bot.db.subscription import Subscription
from bot.db.make_models import async_session

from sqlalchemy import select, delete


async def add_subscription(user_id: int, town: str, chat_id: int):
    async with async_session() as session:
        session.add(
            Subscription(telegram_id=user_id, is_subscribed=True, chat_id=chat_id)
        )
        # await session.commit()
        subscription_id = await session.scalar(
            select(Subscription.id).where(Subscription.telegram_id == user_id)
        )
        town_id = await session.scalar(select(Town.id).where(Town.town == town))
        session.add(
            SubscriptionTownAssociation(
                subscription_id=subscription_id, town_id=town_id
            )
        )
        await session.commit()


async def check_user_sub(user_id: int) -> bool:
    async with async_session() as session:
        is_subscribed = await session.scalar(
            select(Subscription.is_subscribed).where(
                Subscription.telegram_id == user_id
            )
        )

        return is_subscribed


async def sub_user(user_id: int, town: str):
    async with async_session() as session:
        session.add(Subscription(telegram_id=user_id, is_subscribed=True, town=town))
        await session.commit()


async def unsub_user(user_id: int):
    async with async_session() as session:
        await session.execute(
            delete(Subscription).where(Subscription.telegram_id == user_id)
        )
        await session.commit()


async def delete_subscription(user_id: int):
    async with async_session() as session:
        await session.execute(
            delete(Subscription).where(Subscription.telegram_id == user_id)
        )
        await session.commit()


async def get_user():
    async with async_session as session:
        result = await session.execute(select(Subscription))

        return result.fetchall()
