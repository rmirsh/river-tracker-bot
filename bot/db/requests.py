import asyncio

from bot.db.models import Subscription, async_session
from sqlalchemy import select, delete


async def check_user_sub(user_id: int):
    async with async_session() as session:
        is_subscribed = await session.scalar(select(Subscription.is_subscribed).where(Subscription.telegram_id == user_id))

        return is_subscribed


async def sub_user(user_id: int):
    async with async_session() as session:
        session.add(Subscription(telegram_id=user_id, is_subscribed=True))
        await session.commit()


async def unsub_user(user_id: int):
    async with async_session() as session:
        await session.execute(delete(Subscription).where(Subscription.telegram_id == user_id))
        await session.commit()
