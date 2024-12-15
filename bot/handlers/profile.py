from aiogram import types, Dispatcher
from bot.utils.db import get_user
from bot.utils.i18n import i18n

async def cmd_profile(message: types.Message):
    user = get_user(message.from_user.id)
    lang = user.language if user else "ru"
    if not user:
        await message.answer("User not found.")
        return
    text = (
        f"Ваш профиль:\n"
        f"Имя: {user.name}\n"
        f"Город: {user.city}\n"
        f"Контакт: {user.contact}\n"
        f"Роль: {user.role}\n"
        f"Категория услуг: {user.service_category or '-'}\n"
        f"Опыт: {user.experience or '-'}\n"
        f"Регион: {user.region or '-'}\n"
        f"Рейтинг: {user.rating}\n"
    )
    await message.answer(text)

def register_profile_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_profile, commands="profile")
