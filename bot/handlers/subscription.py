from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.db.crud import requests
from bot.utils.keyboards import make_row_keyboard
from bot.utils.states import SubscriptionState
from parser import river_parser

router = Router()


@router.message(StateFilter(None), Command("subscribe"))
async def cmd_subscribe(message: types.Message, state: FSMContext):
    """Subscribe to receive notifications for water level reaching a dangerous
    point.

    This function clears the current state, asks the user if they want to
    subscribe for notifications to be sent every 30 minutes when the water
    level reaches a dangerous point, and sets the state for setting up the
    subscription.

    Args:
        message (types.Message): The message object triggering the command.
        state (FSMContext): The state machine context for managing user state.
    """

    await state.clear()
    await message.answer(
        "Я могу отправлять Вам уведомления каждые 30 минут, "
        "когда вода поднимется до опасного уровня.\n\n"
        "Хотите подписаться на уведомления?\n",
        reply_markup=make_row_keyboard(["Да", "Нет"]),
    )
    await state.set_state(SubscriptionState.setting_sub)


@router.message(SubscriptionState.setting_sub, F.text == "Да")
async def subscription_done(message: types.Message, state: FSMContext):
    """Update the subscription data in the state and prompt the user to choose
    their town.

    Args:
        message (types.Message): The message object containing the subscription information.
        state (FSMContext): The state object to update with the subscription data.
    """

    await state.update_data(subscription=message.text.lower())
    await message.answer(
        "Выберите Ваш населённый пункт.\n", reply_markup=make_row_keyboard(river_parser.towns)
    )
    await state.set_state(SubscriptionState.choosing_town)


@router.message(SubscriptionState.setting_sub, F.text == "Нет")
async def unsubscription_done(message: types.Message, state: FSMContext):
    """Update user subscription status to unsubscribe.

    Updates the user subscription status to unsubscribe based on the message
    received. If the user was subscribed, the subscription is deleted from
    the database.

    Args:
        message (types.Message): The message object containing the user input.
        state (FSMContext): The state context for managing user conversation state.
    """

    await state.update_data(subscription=message.text.lower())
    await message.answer(
        "Вам не будут приходить уведомления.\n"
        "Если передумаете, то отправьте команду /subscribe",
        reply_markup=ReplyKeyboardRemove(),
    )
    if requests.check_subscription(message.from_user.id):
        await requests.delete_subscription(message.from_user.id)

    await state.clear()


@router.message(SubscriptionState.setting_sub)
async def subscription_done_incorrectly(message: types.Message):
    """Display a message asking the user to choose between 'да' or 'нет'.

    Args:
        message (types.Message): The message object triggering this function.
    """

    await message.answer(
        "Пожалуйста выберите один из вариантов ниже.\n",
        reply_markup=make_row_keyboard(["да", "нет"]),
    )


@router.message(SubscriptionState.choosing_town, F.text.in_(river_parser.towns))
async def town_chosed(message: types.Message, state: FSMContext):
    """Notify user about receiving notifications every 30 minutes when the
    water level
    in the chosen town reaches dangerous levels.

    Args:
        message (types.Message): The message object containing user input.
        state (FSMContext): The state of the conversation flow.
    """

    await message.answer(
        f"Вам будут приходить уведомления каждые 30 минут, когда уровень воды "
        f"в населённом пункте {message.text} достигнет опасных значений.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await requests.add_subscription(message.from_user.id, message.text, message.chat.id)
    await state.clear()


@router.message(SubscriptionState.choosing_town)
async def town_chosed_incorrectly(message: types.Message):
    """Inform the user that the chosen town is not in the list of available
    towns.

    This function sends a message to the user indicating that the chosen
    town is not in the list of available towns. It prompts the user to click
    a button below.

    Args:
        message (types.Message): The message object triggering this function.
    """

    await message.answer(
        "В моем списке населённых пунктов пока что такого нет.\n\n"
        " Пожалуйста, нажмите на кнопку ниже.",
        reply_markup=make_row_keyboard(river_parser.towns),
    )
