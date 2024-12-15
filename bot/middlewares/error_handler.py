# bot/middlewares/error_handler.py

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import Dispatcher
from bot.utils.logger import logger
from bot.utils.config_reader import config


class ErrorHandlerMiddleware(BaseMiddleware):
    async def on_error(self, update: types.Update, exception: Exception, data: dict):
        logger.exception(f"Ошибка при обработке обновления: {update} | Исключение: {exception}")

        # Отправляем сообщение администратору о критической ошибке
        admin_ids = config.ADMIN_IDS
        for admin_id in admin_ids:
            try:
                if isinstance(update, types.Message):
                    await update.bot.send_message(admin_id, f"Ошибка: {exception}\nОбновление: {update.text}")
                elif isinstance(update, types.CallbackQuery):
                    await update.bot.send_message(admin_id, f"Ошибка: {exception}\nОбновление: CallbackQuery")
                else:
                    await update.bot.send_message(admin_id, f"Ошибка: {exception}\nОбновление: {update}")
            except Exception as e:
                logger.exception(f"Не удалось отправить сообщение администратору {admin_id}: {e}")

        # Прекращаем обработку текущего обновления
        raise CancelHandler()
