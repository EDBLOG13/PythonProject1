# bot/states/review_states.py

from aiogram.dispatcher.filters.state import State, StatesGroup

class ReviewStates(StatesGroup):
    specialist_id = State()
    rating = State()
    text = State()
