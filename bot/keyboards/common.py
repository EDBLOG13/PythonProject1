# bot/keyboards/common.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.i18n import i18n

def client_main_menu(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(text=i18n.t("btn_search_specialist", lang), callback_data="search_specialist"),
        InlineKeyboardButton(text=i18n.t("btn_new_order", lang), callback_data="new_order")
    )
    kb.add(
        InlineKeyboardButton(text=i18n.t("btn_my_orders", lang), callback_data="my_orders"),
        InlineKeyboardButton(text=i18n.t("btn_profile", lang), callback_data="profile")
    )
    kb.add(
        InlineKeyboardButton(text=i18n.t("btn_leave_review", lang), callback_data="leave_review"),
        InlineKeyboardButton(text=i18n.t("btn_change_language", lang), callback_data="change_language")
    )
    return kb

def specialist_main_menu(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(text="📝 Новые заказы", callback_data="view_new_orders"),
        InlineKeyboardButton(text="⚙️ Ред. профиль", callback_data="edit_profile")
    )
    kb.add(
        InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
        InlineKeyboardButton(text=i18n.t("btn_change_language", lang), callback_data="change_language")
    )
    return kb

def admin_main_menu(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(text="👥 Пользователи", callback_data="users_list"),
        InlineKeyboardButton(text="📊 Статистика заказов", callback_data="orders_stat")
    )
    kb.add(
        InlineKeyboardButton(text="⭐ Отзывы (модерация)", callback_data="reviews_moderation")
    )
    kb.add(
        InlineKeyboardButton(text="🚫 Заблокировать", callback_data="block_user"),
        InlineKeyboardButton(text="✅ Разблокировать", callback_data="unblock_user")
    )
    kb.add(
        InlineKeyboardButton(text=i18n.t("btn_change_language", lang), callback_data="change_language")
    )
    return kb
