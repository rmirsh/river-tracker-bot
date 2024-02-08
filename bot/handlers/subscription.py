from aiogram import Router, types, F
from aiogram.filters import Command

from bot.db import requests
from bot.keyboards import sub_kb

router = Router()


@router.message(Command('subscribe'))
async def cmd_subscribe(message: types.Message):
    await message.answer(
        "Я могу отправлять Вам уведомления каждые 30 минут, "
        "когда вода поднимется до опасного уровня.\n\n"
        "Хотите подписаться на уведомления?",
        reply_markup=sub_kb()
    )


@router.callback_query(F.data == 'subscribe')
async def subscribe(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    sub = await requests.check_user_sub(user_id)

    if not sub:
        await requests.sub_user(user_id)
        await callback.message.answer("Готово! Вы подписаны.")
    else:
        await callback.message.answer("Вы уже подписаны.")

    await callback.answer()


@router.callback_query(F.data == 'unsubscribe')
async def unsubscribe(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    sub = await requests.check_user_sub(user_id)

    if sub:
        await requests.unsub_user(user_id)
        await callback.message.answer("Готово! Вы отписаны.")
    else:
        await callback.message.answer("Вы ещё не подписаны.")
