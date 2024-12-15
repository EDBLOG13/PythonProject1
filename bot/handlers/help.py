from aiogram import types, Dispatcher
from bot.utils.db import get_user
from bot.utils.i18n import i18n

async def cmd_help(message: types.Message):
    user = get_user(message.from_user.id)
    lang = user.language if user else "ru"
    text = (
        "/start - перезапустить бота\n"
        "/help - помощь\n"
        "/search <услуга> - Поиск специалистов\n"
        "/new_order - Создать новую заявку\n"
        "/my_orders - Просмотр моих заявок\n"
        "/complete_order <ID> - Отметить заказ выполненным\n"
        "/leave_review <ID_специалиста> <оценка> <текст> - Оставить отзыв\n"
        "/notifications - Вкл/выкл уведомления\n"
        "/profile - Просмотр профиля\n"
        "/admin - Панель администратора\n"
    )
    await message.answer(text)

def register_help_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_help, commands="help")
