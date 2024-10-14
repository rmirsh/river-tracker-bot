from bot.db import SubscriptionTownAssociation
from bot.db import Town
from bot.db import Subscription
from bot.db.db_manager import db_manager

from sqlalchemy import select, delete, update


async def add_subscription(user_id: int, town: str, chat_id: int):
    """Add a new subscription for a user in a specific town.

    This function adds a new subscription for a user in a specific town by
    creating entries in the database for Subscription and
    SubscriptionTownAssociation.

    Args:
        user_id (int): The unique identifier of the user.
        town (str): The name of the town for which the user is subscribing.
        chat_id (int): The chat ID associated with the subscription.
    """

    async for session in db_manager.session_getter():
        await session.execute(
            update(Subscription)
            .where(Subscription.telegram_id == user_id)
            .values(is_subscribed=True, chat_id=chat_id)
        )
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


async def delete_subscription(user_id: int):
    """Delete a subscription for a user based on the user ID.

    Args:
        user_id (int): The ID of the user whose subscription needs to be deleted.
    """

    async for session in db_manager.session_getter():
        await session.execute(
            update(Subscription)
            .where(Subscription.telegram_id == user_id)
            .values(is_subscribed=False)
        )
        await session.commit()


async def check_subscription(user_id: int) -> bool:
    """Check if a user is subscribed.

    This function checks if a user with the given user_id is subscribed by
    querying the database.

    Args:
        user_id (int): The user ID to check subscription for.

    Returns:
        bool: True if the user is subscribed, False otherwise.
    """

    async for session in db_manager.session_getter():
        is_subscribed = await session.scalar(
            select(Subscription.is_subscribed).where(
                Subscription.telegram_id == user_id
            )
        )

        return is_subscribed


async def get_all_users():
    """Retrieve a list of users from the database.

    This function asynchronously fetches a list of users from the database
    using an async session.

    Returns:
        list: A list of user objects retrieved from the database.
    """

    async for session in db_manager.session_getter():
        query = select(SubscriptionTownAssociation)
        result = await session.execute(query)
        users = result.all()

        return users


async def get_subs_chat_id_and_town():
    """Retrieve the chat ID and town information for all subscriptions.

    This function queries the database to fetch the chat ID and
    corresponding town information for all subscriptions. It performs a join
    operation between the Subscription, SubscriptionTownAssociation, and
    Town tables to gather the required data.

    Returns:
        list: A list of tuples containing chat ID and town information for each
            subscription.
    """

    async for session in db_manager.session_getter():
        result = await session.execute(
            select(Subscription.chat_id, Town.town)
            .join(
                SubscriptionTownAssociation,
                Subscription.id == SubscriptionTownAssociation.subscription_id,
            )
            .join(Town, Town.id == SubscriptionTownAssociation.town_id)
        )
        subs_and_towns = result.all()

    return subs_and_towns


async def is_first_time(user_id: int) -> bool:
    """Check if a user is subscribed.

    This function checks if a user with the given user_id is first time using bot by
    querying the database.

    Args:
        user_id (int): The user ID to check subscription for.

    Returns:
        is_first_time (bool): True if the user is first time using bot, False otherwise.
    """

    async for session in db_manager.session_getter():
        first_time = await session.scalar(
            select(Subscription.is_first_time).where(
                Subscription.telegram_id == user_id
            )
        )
        if not await is_user_exists(user_id):
            return True

    return first_time


async def is_user_exists(user_id: int) -> bool:
    """Check if a user exists in the database.

    This function checks if a user with the given user_id exists in the
    database by querying the database.

    Args:
        user_id (int): The user ID to check for existence.

    Returns:
        bool: True if the user exists in the database, False otherwise.
    """

    async for session in db_manager.session_getter():
        exists = await session.scalar(
            select(Subscription).where(Subscription.telegram_id == user_id)
        )

    return bool(exists)


async def set_first_time(user_id: int) -> None:
    """Set the first time flag for a user.

    This function sets the first time flag for a user with the given user_id
    in the database.

    Args:
        user_id (int): The user ID for which the first time flag needs to be set.
    """

    async for session in db_manager.session_getter():
        if await is_user_exists(user_id):
            await session.execute(
                update(Subscription)
                .where(Subscription.telegram_id == user_id)
                .values(is_first_time=False)
            )
        else:
            session.add(
                Subscription(
                    telegram_id=user_id,
                    chat_id=user_id,
                    is_subscribed=False,
                    is_first_time=False,
                )
            )
        await session.commit()
