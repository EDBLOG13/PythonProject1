# bot/handlers/__init__.py

from aiogram import Dispatcher
from .start import register_start_handlers
from .search import register_search_handlers
from .orders import register_orders_handlers
from .reviews import register_reviews_handlers
from .menu import register_menu_handlers
from .profile import register_profile_handlers
from .language import register_language_handlers
# Импортируйте другие хендлеры здесь и регистрируйте их

def register_all_handlers(dp: Dispatcher):
    register_start_handlers(dp)
    register_search_handlers(dp)
    register_orders_handlers(dp)
    register_reviews_handlers(dp)
    register_menu_handlers(dp)
    register_profile_handlers(dp)
    register_language_handlers(dp)
    # Зарегистрируйте другие хендлеры здесь
