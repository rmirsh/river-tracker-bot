from aiogram.fsm.state import StatesGroup, State


class RemoveSubscriptionState(StatesGroup):
    remove_all_or_specific = State()
    choosing_town = State()
    remove_sub = State()
