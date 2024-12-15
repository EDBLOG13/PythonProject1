# bot/main.py

import logging
import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers import register_all_handlers
from bot.utils.logger import logger
from bot.utils.config_reader import config

# Получение токена бота из переменных окружения
API_TOKEN = os.getenv("BOT_TOKEN")  # Изменено: BOT_API_TOKEN на BOT_TOKEN согласно .env

if not API_TOKEN:
    logger.error("BOT_TOKEN не задан в переменных окружения.")
    exit(1)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Регистрация всех хендлеров
register_all_handlers(dp)

if __name__ == "__main__":
    logger.info("Бот запускается...")
    executor.start_polling(dp, skip_updates=True)
