# bot/states/order_states.py

from aiogram.dispatcher.filters.state import State, StatesGroup

class OrderStates(StatesGroup):
    description = State()
    category = State()
    preferred_time = State()
    location = State()
