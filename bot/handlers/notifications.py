from aiogram import types, Dispatcher
from bot.utils.db import get_user, update_user
from bot.utils.i18n import i18n

async def cmd_notifications(message: types.Message):
    user = get_user(message.from_user.id)
    lang = user.language
    # Переключаем уведомления
    current_state = getattr(user, "notification_enabled", True)
    new_state = not current_state
    update_user(user.telegram_id, notification_enabled=new_state)
    if new_state:
        await message.answer(i18n.t("notifications_on", lang))
    else:
        await message.answer(i18n.t("notifications_off", lang))

async def respond_callback(call: types.CallbackQuery):
    user = get_user(call.from_user.id)
    lang = user.language
    if user.role != "specialist":
        await call.answer(i18n.t("no_permission", lang), show_alert=True)
        return

    parts = call.data.split("_")
    if len(parts) != 2:
        await call.answer("Error", show_alert=True)
        return
    # В данном примере просто уведомляем специалиста, что отклик зарегистрирован
    await call.answer(i18n.t("response_received", lang), show_alert=True)

def register_notifications_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_notifications, commands="notifications")

def register_responses_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(respond_callback, lambda c: c.data.startswith("respond_"))
