# bot/handlers/menu.py

from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
from bot.utils.db import get_user
from bot.utils.i18n import i18n
from bot.keyboards.common import client_main_menu, specialist_main_menu, admin_main_menu
from bot.utils.logger import logger
from aiogram.dispatcher import FSMContext

# Импортируйте необходимые хендлеры
from bot.handlers.search import cmd_search_specialist_prompt
from bot.handlers.orders import cmd_new_order, cmd_my_orders
from bot.handlers.profile import cmd_profile
from bot.handlers.reviews import cmd_leave_review_prompt
from bot.handlers.language import cmd_change_language

async def menu_handler(callback_query: CallbackQuery, state: FSMContext):
    user = get_user(callback_query.from_user.id)
    if not user:
        await callback_query.message.answer("Пожалуйста, начните с /start")
        await callback_query.answer()
        return

    lang = user.language
    role = user.role

    data = callback_query.data

    if role == "client":
        if data == "search_specialist":
            await cmd_search_specialist_prompt(callback_query.message, state)
        elif data == "new_order":
            await cmd_new_order(callback_query.message, state)
        elif data == "my_orders":
            await cmd_my_orders(callback_query.message, state)
        elif data == "profile":
            await cmd_profile(callback_query.message, state)
        elif data == "leave_review":
            await cmd_leave_review_prompt(callback_query.message, state)
        elif data == "change_language":
            await cmd_change_language(callback_query.message, state)
        else:
            await callback_query.message.answer(i18n.t("main_menu_client", lang), reply_markup=client_main_menu(lang))
    elif role == "specialist":
        # Реализуйте аналогично для специалиста
        await callback_query.message.answer("Меню для специалиста ещё не реализовано.")
    elif role == "admin":
        # Реализуйте аналогично для админа
        await callback_query.message.answer("Меню для администратора ещё не реализовано.")
    else:
        await callback_query.message.answer("Неизвестная роль. Пожалуйста, начните заново с /start")

    await callback_query.answer()

def register_menu_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(menu_handler, lambda c: c.data in [
        "search_specialist",
        "new_order",
        "my_orders",
        "profile",
        "leave_review",
        "change_language"
    ], state="*")
