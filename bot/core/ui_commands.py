from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand

bot_commands = (
    BotCommand(command="start", description="Запустить бота"),
    BotCommand(command="subscribe", description="Подписаться на уведомления"),
    BotCommand(command="donate", description="Сделать пожертвование"),
)


async def set_ui_commands(bot: Bot):
    """Set the UI commands for the bot.

    This function sets the UI commands for the bot using the provided Bot
    instance.

    Args:
        bot (Bot): The Bot instance to set the commands for.
    """
    await bot.set_my_commands(commands=bot_commands, scope=BotCommandScopeAllPrivateChats())
