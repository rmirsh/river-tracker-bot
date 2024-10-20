from aiogram.fsm.state import StatesGroup, State


class SubscriptionState(StatesGroup):
    set_sub = State()
    choosing_town = State()
