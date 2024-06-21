from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand


async def set_ui_commands(bot: Bot):
    """Set the UI commands for the bot.

    This function sets the UI commands for the bot using the provided Bot
    instance.

    Args:
        bot (Bot): The Bot instance to set the commands for.
    """

    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="subscribe", description="Подписаться на уведомления"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
