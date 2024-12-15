# bot/utils/i18n.py

import json
import os
from bot.utils.config_reader import config
from typing import Dict

class I18n:
    def __init__(self, locale_dir: str = None, default_lang: str = "ru"):
        if locale_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            locale_dir = os.path.join(base_dir, "locale")
        self.locale_dir = locale_dir
        self.default_lang = default_lang
        self.translations = {}
        self._load_translations()

    def _load_translations(self):
        for lang in ["ru", "uz"]:
            path = os.path.join(self.locale_dir, f"{lang}.json")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.translations[lang] = json.load(f)
            except FileNotFoundError:
                logger.error(f"Файл перевода для языка '{lang}' не найден по пути: {path}")
                self.translations[lang] = {}
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка декодирования JSON в файле {path}: {e}")
                self.translations[lang] = {}

    def t(self, key: str, lang: str = None, **kwargs) -> str:
        lang = lang or self.default_lang
        text = self.translations.get(lang, {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError as e:
                logger.error(f"Отсутствует ключ для форматирования: {e}")
                return text
        return text

i18n = I18n(default_lang=config.DEFAULT_LANG)
