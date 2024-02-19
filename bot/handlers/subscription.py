from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.db import requests
from bot.keyboards import make_row_keyboard
from bot.utils.states import SubscriptionState
from emercit_parse.emercit_data import towns

router = Router()


@router.message(StateFilter(None), Command('subscribe'))
async def cmd_subscribe(message: types.Message, state: FSMContext):
    await message.answer(
        "Я могу отправлять Вам уведомления каждые 30 минут, "
        "когда вода поднимется до опасного уровня.\n\n"
        "Хотите подписаться на уведомления?\n",
        reply_markup=make_row_keyboard(["Да", "Нет"])
    )
    await state.set_state(SubscriptionState.setting_sub)


@router.message(
    SubscriptionState.setting_sub,
    F.text == "Да"
)
async def subscription_done(message: types.Message, state: FSMContext):
    await state.update_data(subscription=message.text.lower())
    await message.answer(
        "Выберите Ваш населённый пункт.\n",
        reply_markup=make_row_keyboard(towns)
    )
    await state.set_state(SubscriptionState.choosing_town)


@router.message(
    SubscriptionState.setting_sub,
    F.text == "Нет"
)
async def subscription_done(message: types.Message, state: FSMContext):
    await state.update_data(subscription=message.text.lower())
    await message.answer(
        "Вам не будут приходить уведомления.\n"
        "Если передумаете, то отправьте команду /subscribe",
        reply_markup=ReplyKeyboardRemove()
    )
    if requests.check_user_sub(message.from_user.id):
        await requests.delete_subscription(message.from_user.id)

    await state.clear()


@router.message(SubscriptionState.setting_sub)
async def subscription_done_incorrectly(message: types.Message):
    await message.answer(
        "Пожалуйста выберите один из вариантов ниже.\n",
        reply_markup=make_row_keyboard(["да", "нет"])
    )


@router.message(
    SubscriptionState.choosing_town,
    F.text.in_(towns)
)
async def town_chosed(message: types.Message, state: FSMContext):
    await message.answer(
        f"Вам будут приходить уведомления каждые 30 минут, когда уровень воды "
        f"в населённом пункте {message.text} достигнет опасных значений.",
        reply_markup=ReplyKeyboardRemove()
    )
    await requests.add_subscription(message.from_user.id, message.text)
    await state.clear()


@router.message(
    SubscriptionState.choosing_town
)
async def town_chosed_incorrectly(message: types.Message):
    await message.answer(
        "В моем списке населённых пунктов пока что такого нет.\n\n"
        " Пожалуйста, нажмите на кнопку ниже.",
        reply_markup=make_row_keyboard(towns)
    )
