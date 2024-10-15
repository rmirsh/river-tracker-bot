from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import ReplyKeyboardRemove

from bot.core.lexicon import lexicon_ru
from bot.db.crud.requests import is_first_time, set_first_time
from parser import river_parser

router = Router()


@router.message(StateFilter(None), CommandStart())
async def cmd_start(message: types.Message):
    """Start command handler for the bot.

    Greets the user with a personalized message and prompts them to select a
    town.

    Args:
        message (types.Message): The message object containing user information.
    """

    await message.answer(
        lexicon_ru["/start"]["welcome-msg"].format(name=message.from_user.full_name),
        reply_markup=ReplyKeyboardRemove(),
    )

    if await is_first_time(message.from_user.id):
        await set_first_time(message.from_user.id)
        await message.answer(lexicon_ru["/start"]["donate-msg"])
