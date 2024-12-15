# bot/states/search_states.py

from aiogram.dispatcher.filters.state import State, StatesGroup

class SearchStates(StatesGroup):
    category = State()
