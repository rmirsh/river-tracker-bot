from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand

commands = {
    "/start": "Запустить бота",
    "/subscribe": "Подписаться на уведомления",
    "/donate": "Сделать пожертвование",
    "/get_data": "Получить данные об уровне реки",
}


async def set_ui_commands(bot: Bot):
    """Set the UI commands for the bot.

    This function sets the UI commands for the bot using the provided Bot
    instance.

    Args:
        bot (Bot): The Bot instance to set the commands for.
    """
    bot_commands = [BotCommand(command=key, description=value) for key, value in commands.items()]

    await bot.set_my_commands(commands=bot_commands, scope=BotCommandScopeAllPrivateChats())
