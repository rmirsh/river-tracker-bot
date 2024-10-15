from aiogram import Router, types, F
from aiogram.filters import CommandStart

from bot.core.lexicon import lexicon_ru
from bot.db.crud.requests import is_first_time, set_first_time
from bot.core.keyboards import get_town_kb
from parser import river_parser

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Start command handler for the bot.

    Greets the user with a personalized message and prompts them to select a
    town.

    Args:
        message (types.Message): The message object containing user information.
    """

    await message.answer(lexicon_ru["/start"].format(name=message.from_user.full_name))

    if await is_first_time(message.from_user.id):
        await set_first_time(message.from_user.id)
        await message.answer(lexicon_ru["/donate"])


@router.callback_query(F.data.in_(river_parser.town_mapper))
async def send_river_data(callback: types.CallbackQuery):
    """Send river data information based on the current river level compared to
    danger and prevention levels.

    Args:
        callback (types.CallbackQuery): The callback query object.
    """

    river_data = await river_parser.fetch_river_data(callback.data)

    if river_data.current_river_level >= river_data.danger_level:
        answer_message = (
            f"<b>‼️️ОПАСНОСТЬ‼️\n<u>На {river_data.date} в {river_data.time} "
            f"в Вашем населённом пункте текущий уровень воды превышает опасный "
            f"уровень воды.</u></b>"
        )
        await callback.message.answer(answer_message)

    elif river_data.current_river_level >= river_data.prevention_level:
        answer_message = (
            f"<b>❗️УГРОЗА❗️\nНа {river_data.date} в {river_data.time} "
            f"в Вашем населённом пункте текущий уровень воды превышает "
            f"предупредительный уровень воды.</b>"
        )
        await callback.message.answer(answer_message)

    await callback.message.answer(
        f"<u>На {date} в {time}, в населённом пункте <i>{callback.data}</i>:</u>\n"
        f"Текущий уровень воды: <b>{river_data.current_river_level} м</b>\n"
        f"Предупредительный уровень воды: <b>{river_data.prevention_level} м</b>\n"
        f"Опасный уровень воды: <b>{river_data.danger_level} м</b>\n"
    )

    await callback.answer()
