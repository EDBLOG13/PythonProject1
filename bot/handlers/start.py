# bot/handlers/start.py

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot.states.registration_states import RegistrationStates
from bot.utils.db import get_user, create_user
from bot.utils.i18n import i18n
from bot.keyboards.common import client_main_menu, specialist_main_menu, admin_main_menu
from bot.utils.logger import logger  # Импортируем логгер


async def cmd_start(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} начал сессию /start")
    user = get_user(message.from_user.id)
    if user:
        if user.blocked:
            await message.answer("Вы заблокированы.")
            logger.warning(f"Заблокированный пользователь {message.from_user.id} попытался использовать бота.")
            return
        lang = user.language
        await show_main_menu(message, user.role, lang)
        logger.info(f"Пользователь {message.from_user.id} вошёл в главное меню как {user.role}")
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Русский", "O'zbekcha")
        await message.answer(i18n.t("choose_language"), reply_markup=keyboard)
        await RegistrationStates.language.set()
        logger.info(f"Пользователь {message.from_user.id} начал регистрацию и выбрал язык.")


async def registration_language(message: types.Message, state: FSMContext):
    logger.debug(f"Пользователь {message.from_user.id} выбирает язык: {message.text}")
    chosen = message.text.lower()
    if "rus" in chosen:
        lang = "ru"
    elif "o'z" in chosen or "uz" in chosen:
        lang = "uz"
    else:
        await message.answer("Пожалуйста, выберите язык из доступных вариантов.")
        logger.warning(f"Пользователь {message.from_user.id} выбрал недопустимый язык: {message.text}")
        return
    await state.update_data(language=lang)
    await message.answer(i18n.t("language_chosen", lang), reply_markup=types.ReplyKeyboardRemove())
    await message.answer(i18n.t("start_welcome", lang))
    await message.answer(i18n.t("ask_name", lang))
    await RegistrationStates.name.set()
    logger.info(f"Пользователь {message.from_user.id} выбрал язык: {lang}")


async def registration_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["language"]
    name = message.text.strip()
    await state.update_data(name=name)
    await message.answer(i18n.t("ask_city", lang))
    await RegistrationStates.city.set()
    logger.info(f"Пользователь {message.from_user.id} ввёл имя: {name}")


async def registration_city(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["language"]
    city = message.text.strip()
    await state.update_data(city=city)
    await message.answer(i18n.t("ask_contact", lang))
    await RegistrationStates.contact.set()
    logger.info(f"Пользователь {message.from_user.id} ввёл город: {city}")


async def registration_contact(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["language"]
    contact = message.text.strip()
    await state.update_data(contact=contact)
    await message.answer(i18n.t("ask_role", lang))
    await RegistrationStates.role.set()
    logger.info(f"Пользователь {message.from_user.id} ввёл контакт: {contact}")


async def registration_role(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["language"]
    role_response = message.text.lower()
    if role_response in ["да", "ha"]:
        await message.answer(i18n.t("ask_service_category", lang))
        await RegistrationStates.service_category.set()
        logger.info(f"Пользователь {message.from_user.id} выбрал роль: специалист")
    else:
        user_id = create_user(
            telegram_id=message.from_user.id,
            name=data["name"],
            city=data["city"],
            contact=data["contact"],
            role="client",
            language=lang
        )
        await message.answer(i18n.t("registration_complete_client", lang),
                             reply_markup=client_main_menu(lang))
        logger.info(f"Пользователь {message.from_user.id} зарегистрирован как клиент с ID {user_id}")
        await state.finish()


async def registration_service_category(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["language"]
    service_category = message.text.strip()
    await state.update_data(service_category=service_category)
    await message.answer(i18n.t("ask_experience", lang))
    await RegistrationStates.experience.set()
    logger.info(f"Пользователь {message.from_user.id} ввёл категорию услуг: {service_category}")


async def registration_experience(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["language"]
    experience = message.text.strip()
    await state.update_data(experience=experience)
    await message.answer(i18n.t("ask_region", lang))
    await RegistrationStates.region.set()
    logger.info(f"Пользователь {message.from_user.id} ввёл опыт: {experience}")


async def registration_region(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data["language"]
    region = message.text.strip()
    role = "specialist"
    service_category = data.get("service_category")
    experience = data.get("experience")

    user_id = create_user(
        telegram_id=message.from_user.id,
        name=data["name"],
        city=data["city"],
        contact=data["contact"],
        role=role,
        language=lang,
        service_category=service_category,
        experience=experience,
        region=region
    )
    await message.answer(i18n.t("registration_complete_specialist", lang),
                         reply_markup=specialist_main_menu(lang))
    logger.info(f"Пользователь {message.from_user.id} зарегистрирован как специалист с ID {user_id}")
    await state.finish()


async def show_main_menu(message: types.Message, role: str, lang: str):
    if role == "client":
        await message.answer(i18n.t("returning_user", lang), reply_markup=client_main_menu(lang))
        logger.info(f"Показано клиентское меню пользователю {message.from_user.id}")
    elif role == "specialist":
        await message.answer(i18n.t("returning_user", lang), reply_markup=specialist_main_menu(lang))
        logger.info(f"Показано меню специалиста пользователю {message.from_user.id}")
    elif role == "admin":
        await message.answer(i18n.t("main_menu_admin", lang), reply_markup=admin_main_menu(lang))
        logger.info(f"Показано меню администратора пользователю {message.from_user.id}")
    else:
        await message.answer(i18n.t("returning_user", lang), reply_markup=client_main_menu(lang))
        logger.warning(f"Пользователь {message.from_user.id} имеет неизвестную роль: {role}")


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(registration_language, state=RegistrationStates.language)
    dp.register_message_handler(registration_name, state=RegistrationStates.name)
    dp.register_message_handler(registration_city, state=RegistrationStates.city)
    dp.register_message_handler(registration_contact, state=RegistrationStates.contact)
    dp.register_message_handler(registration_role, state=RegistrationStates.role)
    dp.register_message_handler(registration_service_category, state=RegistrationStates.service_category)
    dp.register_message_handler(registration_experience, state=RegistrationStates.experience)
    dp.register_message_handler(registration_region, state=RegistrationStates.region)
