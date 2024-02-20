from bot.db.town import Town
from bot.db.subscription import Subscription
from bot.db.make_models import async_session

from sqlalchemy import select, delete


async def check_user_sub(user_id: int):
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


async def add_subscription(user_id: int, town: str):
    async with async_session() as session:
        session.add(Subscription(telegram_id=user_id, is_subscribed=True))
        value = await session.scalar(
            select(Subscription.id).where(Subscription.telegram_id == user_id)
        )
        session.add(Town(town=town, subs_id=value))
        await session.commit()


async def delete_subscription(user_id: int):
    async with async_session() as session:
        await session.execute(
            delete(Subscription).where(Subscription.telegram_id == user_id)
        )
        await session.commit()
