from aiogram import types, Router, F
from aiogram.filters import StateFilter, Command

from bot.core.keyboards import get_town_kb
from bot.core.lexicon import lexicon_ru
from parser import river_parser

router = Router()


@router.message(StateFilter(None), Command("get_data"))
async def get_data(message: types.Message):
    """Send a message when the command /get_data is issued.

    Args:
        message (types.Message): The message object containing user information.
    """
    await message.answer(
        lexicon_ru["/get_data"]["info"],
        reply_markup=get_town_kb()
    )


@router.callback_query(F.data.in_(river_parser.town_mapper))
async def send_river_data(callback: types.CallbackQuery):
    """Send river data information based on the current river level compared to
    danger and prevention levels.

    Args:
        callback (types.CallbackQuery): The callback query object.
    """
    try:
        river_data = await river_parser.fetch_river_data(callback.data)

        if river_data.current_river_level >= river_data.danger_level:
            answer_message = lexicon_ru["/get_data"]["danger"].format(
                date=river_data.date,
                time=river_data.time
            )
            await callback.message.answer(answer_message)

        elif river_data.current_river_level >= river_data.prevention_level:
            answer_message = lexicon_ru["/get_data"]["prevention"].format(
                date=river_data.date,
                time=river_data.time
            )
            await callback.message.answer(answer_message)

        await callback.message.answer(
            lexicon_ru["/get_data"]["current"].format(
                town=callback.data,
                date=river_data.date,
                time=river_data.time,
                current_level=river_data.current_river_level,
                prevention_level=river_data.prevention_level,
                danger_level=river_data.danger_level
            )
        )

        await callback.answer()

    except ValueError as e:  # TODO: Сделать кастомные эксепшены
        await callback.message.answer(lexicon_ru["error"])
        raise e
