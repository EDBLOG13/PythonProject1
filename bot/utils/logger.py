# bot/utils/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler

# Определяем директорию для логов
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Корневая папка проекта
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Создаём объект логгера
logger = logging.getLogger("bot_logger")
logger.setLevel(logging.DEBUG)  # Уровень логирования можно настроить

# Форматтер для логов
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Создаём обработчик для записи логов в файл с ротацией
file_handler = RotatingFileHandler(
    filename=os.path.join(LOG_DIR, "bot.log"),
    mode="a",
    maxBytes=5*1024*1024,  # 5 МБ
    backupCount=5,          # Хранить 5 резервных копий
    encoding="utf-8",
    delay=0
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)  # Уровень для файла

# Создаём обработчик для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)  # Уровень для консоли

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)
