# bot/handlers/search.py

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot.utils.db import get_specialists_by_category
from bot.utils.i18n import i18n
from bot.keyboards.common import specialist_main_menu
from bot.utils.logger import logger

async def cmd_search_specialist_prompt(message: types.Message, state: FSMContext):
    await message.answer(i18n.t("category_prompt", message.from_user.language), reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("search_specialist_category")

async def process_search_specialist_category(message: types.Message, state: FSMContext):
    lang = message.from_user.language
    category = message.text.strip()
    specialists = get_specialists_by_category(category)
    if specialists:
        specialists_text = i18n.t("specialists_list", lang)
        for specialist in specialists:
            specialists_text += f"\n🆔 {specialist.id} - {specialist.name} ({specialist.city})"
        await message.answer(specialists_text, reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer(i18n.t("no_specialists_found", lang))
    await state.finish()

def register_search_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_search_specialist_prompt, commands="search_specialist", state="*")
    dp.register_message_handler(process_search_specialist_category, state="search_specialist_category")
