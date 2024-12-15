# bot/handlers/language.py

from aiogram import types, Dispatcher
from bot.utils.db import get_user, update_user
from bot.utils.i18n import i18n
from bot.keyboards.language_menu import language_inline_menu


async def cmd_change_language(message: types.Message, lang: str):
    await message.answer(i18n.t("language_menu_title", lang), reply_markup=language_inline_menu())


async def language_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data.startswith("lang_"):
        new_lang = data.split("_")[1]
        telegram_id = callback_query.from_user.id
        update_user(telegram_id, language=new_lang)

        user = get_user(telegram_id)
        await callback_query.message.edit_text(i18n.t("language_changed", new_lang))

        # Покажем обновлённое меню
        role = user.role
        if role == "client":
            from bot.keyboards.common import client_main_menu
            await callback_query.message.answer(i18n.t("main_menu_client", new_lang),
                                                reply_markup=client_main_menu(new_lang))
        elif role == "specialist":
            from bot.keyboards.common import specialist_main_menu
            await callback_query.message.answer(i18n.t("main_menu_specialist", new_lang),
                                                reply_markup=specialist_main_menu(new_lang))
        elif role == "admin":
            from bot.keyboards.common import admin_main_menu
            await callback_query.message.answer(i18n.t("main_menu_admin", new_lang),
                                                reply_markup=admin_main_menu(new_lang))
        else:
            from bot.keyboards.common import client_main_menu
            await callback_query.message.answer(i18n.t("main_menu_client", new_lang),
                                                reply_markup=client_main_menu(new_lang))

    await callback_query.answer()


def register_language_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_change_language, commands="change_language", state="*")
    dp.register_callback_query_handler(language_callback_handler, lambda c: c.data and c.data.startswith("lang_"))
