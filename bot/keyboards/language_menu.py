# bot/keyboards/language_menu.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def language_inline_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang_uz")
    )
    return kb
