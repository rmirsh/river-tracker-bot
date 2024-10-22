from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.core.keyboards import make_row_keyboard
from bot.core.states import RemoveSubscriptionState
from parser import river_parser

router = Router()


@router.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: types.Message, state: FSMContext):
    """Unsubscribe from receiving notifications."""
    await state.clear()
    await message.answer(
        "Хотите отписаться от уведомлений?",
        reply_markup=make_row_keyboard(["Да", "Нет"]),
    )
    await state.set_state(RemoveSubscriptionState.remove_sub)


@router.message(RemoveSubscriptionState.remove_sub, F.text.lower() == "да")
async def remove_subscription(message: types.Message, state: FSMContext):
    """Remove the subscription from the database and inform the user."""
    await message.answer(
        "Хотите отписаться от всех уведомлений или только от конкретных?",
        reply_markup=make_row_keyboard(["Все", "Конкретные"]),
    )
    await state.set_state(RemoveSubscriptionState.remove_all_or_specific)


@router.message(RemoveSubscriptionState.remove_sub, F.text.lower() == "нет")
async def cancel_remove_subscription(message: types.Message, state: FSMContext):
    """Inform the user that they are not subscribed."""
    await message.answer(
        "Хорошо. Если передумаете — воспользуйтесь командой /unsubscribe.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()


@router.message(RemoveSubscriptionState.remove_all_or_specific, F.text.lower() == "все")
async def remove_all_subscriptions(message: types.Message, state: FSMContext):
    """Remove all subscriptions for the user."""
    # TODO: get user id, delete all subs by id
    await message.answer(
        "Вы отписаны от всех уведомлений.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()


@router.message(RemoveSubscriptionState.remove_all_or_specific, F.text.lower() == "конкретные")
async def choose_town_subscription_to_remove(message: types.Message, state: FSMContext):
    """Prompt the user to enter the town name to unsubscribe from."""
    # TODO: get subs towns, make keyboard with towns
    await message.answer(
        "Введите название населённого пункта, от которого хотите отписаться.",
        reply_markup=make_row_keyboard([str(i) for i in range(1, 11)])
        # TODO: reply_markup=make_row_keyboard(TOWNS)
    )
    await state.set_state(RemoveSubscriptionState.choosing_town)


@router.message(RemoveSubscriptionState.choosing_town)
async def town_chose_incorrectly(message: types.Message, state: FSMContext):
    """Go back to the previous state."""
    await message.answer(
        "Пожалуйста, воспользуйтесь кнопками ниже.",
        # TODO: reply_markup=make_row_keyboard(TOWNS)
    )


@router.message(RemoveSubscriptionState.choosing_town, F.text.in_(river_parser.town_mapper))
async def subscription_removed_successfully(message: types.Message, state: FSMContext):
    """Inform the user that their subscription has been removed."""
    # TODO: remove specific sub by town name
    await message.answer(
        "Вы отписаны от уведомлений об этом населённом пункте.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()


@router.message(RemoveSubscriptionState.choosing_town)
async def subscription_removed_incorrectly(message: types.Message):
    """Inform the user that the input is incorrect."""
    await message.answer(
        "Название населённого пункта введено неверно.\n\n"
        "Пожалуйста, воспользуйтесь кнопками ниже.",
        reply_markup=make_row_keyboard(river_parser.town_mapper)
    )
