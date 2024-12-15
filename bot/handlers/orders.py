# bot/handlers/orders.py

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot.utils.db import get_user, create_order, get_orders
from bot.utils.i18n import i18n
from bot.states.order_states import OrderStates
from bot.keyboards.common import client_main_menu
from bot.utils.logger import logger


async def cmd_new_order(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if user and user.role == "client":
        lang = user.language
        await message.answer(i18n.t("enter_order_desc", lang))
        await OrderStates.description.set()
        logger.info(f"Пользователь {message.from_user.id} начал создание нового заказа.")
    else:
        await message.answer(
            i18n.t("no_permission_create_order", "ru"))  # Убедитесь, что этот ключ существует в переводах
        logger.warning(f"Пользователь {message.from_user.id} попытался создать заказ без прав.")


async def process_order_description(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    lang = user.language if user else "ru"
    description = message.text.strip()
    await state.update_data(description=description)
    await message.answer(i18n.t("enter_order_category", lang))
    await OrderStates.category.set()
    logger.info(f"Пользователь {message.from_user.id} ввёл описание заказа: {description}")


async def process_order_category(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    lang = user.language if user else "ru"
    category = message.text.strip()
    await state.update_data(category=category)
    await message.answer(i18n.t("enter_order_time", lang))
    await OrderStates.preferred_time.set()
    logger.info(f"Пользователь {message.from_user.id} ввёл категорию заказа: {category}")


async def process_order_time(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    lang = user.language if user else "ru"
    preferred_time = message.text.strip()
    await state.update_data(preferred_time=preferred_time)
    await message.answer(i18n.t("enter_order_location", lang))
    await OrderStates.location.set()
    logger.info(f"Пользователь {message.from_user.id} ввёл предпочитаемое время: {preferred_time}")


async def process_order_location(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = get_user(message.from_user.id)
    lang = user.language if user else "ru"
    location = message.text.strip()

    if user:
        order = create_order(
            user_id=user.id,
            description=data.get('description'),
            category=data.get('category'),
            preferred_time=data.get('preferred_time'),
            location=location
        )
        if order:
            await message.answer(i18n.t("order_created", lang))
            logger.info(f"Пользователь {user.id} создал заказ {order.id}.")
        else:
            await message.answer(
                i18n.t("order_creation_failed", lang))  # Убедитесь, что этот ключ существует в переводах
            logger.error(f"Не удалось создать заказ для пользователя {user.id}.")
    else:
        await message.answer(i18n.t("user_not_found", "ru"))  # Убедитесь, что этот ключ существует в переводах
        logger.error(f"Пользователь {message.from_user.id} не найден при создании заказа.")

    await state.finish()


async def cmd_my_orders(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    lang = user.language if user else "ru"
    if user:
        orders = get_orders(user.id)
        if not orders:
            await message.answer(i18n.t("no_orders_found", lang))
            logger.info(f"Пользователь {user.id} запросил заказы, но они не найдены.")
        else:
            orders_text = i18n.t("your_orders", lang)
            for order in orders:
                orders_text += (
                    f"\n\n🆔 {order.id}"
                    f"\n📄 {order.description}"
                    f"\n📂 Категория: {order.category}"
                    f"\n⏰ Время: {order.preferred_time}"
                    f"\n📍 Место: {order.location}"
                    f"\n📌 Статус: {order.status}"
                )
            await message.answer(orders_text)
            logger.info(f"Пользователь {user.id} запросил свои заказы.")
    else:
        await message.answer(i18n.t("user_not_found", "ru"))
        logger.error(f"Пользователь {message.from_user.id} не найден при запросе заказов.")


def register_orders_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_new_order, commands="new_order", state="*")
    dp.register_message_handler(process_order_description, state=OrderStates.description)
    dp.register_message_handler(process_order_category, state=OrderStates.category)
    dp.register_message_handler(process_order_time, state=OrderStates.preferred_time)
    dp.register_message_handler(process_order_location, state=OrderStates.location)
    dp.register_message_handler(cmd_my_orders, commands="my_orders", state="*")
