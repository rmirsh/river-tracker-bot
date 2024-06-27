from aiogram import Router, types, F
from aiogram.filters import CommandStart

from bot.db.requests import is_first_time, set_first_time
from bot.keyboards import get_town_kb
from emercit_parse.async_emercit_parser import async_get_river_data, towns

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Start command handler for the bot.

    Greets the user with a personalized message and prompts them to select a
    town.

    Args:
        message (types.Message): The message object containing user information.
    """

    # await message.answer(
    #     f"Привет, <b>{message.from_user.full_name}</b>! <u><i>Я пока в разработке</i></u>"
    # )
    await message.answer(
        f"Привет, <b>{message.from_user.full_name}</b>!\n"
        "Пожалуйста, выберите населённый пункт.",
        reply_markup=get_town_kb(),
    )

    if await is_first_time(message.from_user.id):
        await set_first_time(message.from_user.id)
        await message.answer(
            "Дорогие друзья! 🌟\n\n"
            "Этот бот создан, чтобы приносить пользу и предупреждать людей об опасности, "
            "а также снять тревожность у пожилых людей и владельцев гаражей вдоль рек. "
            "Его разработкой занимаюсь [я](tg://user?id=446913605), вкладывая в него много времени и усилий. "
            "Если вам нравится моя работа и вы хотите поддержать проект, вы можете сделать пожертвование "
            "(любая удобная Вам сумма). Ваш вклад ❤️ поможет мне продолжать развивать и улучшать сервис, "
            "а также добавлять новые населенные пункты. 🏘️\n\n"
            "Спасибо вам за вашу поддержку и доверие! 🙏"
            "Вы можете сделать донат, воспользовавшись командой /donate."
        )


@router.callback_query(F.data.in_(towns))
async def send_river_data(callback: types.CallbackQuery):
    """Send river data information based on the current river level compared to
    danger and prevention levels.

    Args:
        callback (types.CallbackQuery): The callback query object.
    """

    river_data = await async_get_river_data(callback.data)
    date = river_data.time.split()[0]
    time = river_data.time.split()[1][:-3]

    if river_data.current_river_level >= river_data.danger_level:
        answer_message = f"<b>‼️️ОПАСНОСТЬ‼️\n<u>На {date} в {time} в Вашем населённом пункте текущий уровень воды превышает опасный уровень воды.</u></b>"
        await callback.message.answer(answer_message)

    elif river_data.current_river_level >= river_data.prevention_level:
        answer_message = f"<b>❗️УГРОЗА❗️\nНа {date} в {time} в Вашем населённом пункте текущий уровень воды превышает предупредительный уровень воды.</b>"
        await callback.message.answer(answer_message)

    await callback.message.answer(
        f"<u>На {date} в {time}, в населённом пункте <i>{callback.data}</i>:</u>\n"
        f"Текущий уровень воды: <b>{river_data.current_river_level} м</b>\n"
        f"Предупредительный уровень воды: <b>{river_data.prevention_level} м</b>\n"
        f"Опасный уровень воды: <b>{river_data.danger_level} м</b>\n"
    )

    await callback.answer()
