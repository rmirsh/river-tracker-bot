from aiogram.fsm.state import StatesGroup, State


class SubscriptionState(StatesGroup):
    setting_sub = State()
    choosing_town = State()
