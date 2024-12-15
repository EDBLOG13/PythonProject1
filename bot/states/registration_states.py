# bot/states/registration_states.py

from aiogram.dispatcher.filters.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    language = State()
    name = State()
    city = State()
    contact = State()
    role = State()
    service_category = State()
    experience = State()
    region = State()
