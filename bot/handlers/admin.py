from aiogram import types, Dispatcher
from bot.utils.db import get_user, get_session, User, Order, Review
from bot.utils.i18n import i18n
import os

ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

async def cmd_admin(message: types.Message):
    user = get_user(message.from_user.id)
    lang = user.language if user else "ru"
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(i18n.t("admin_access_denied", lang))
        return
    await message.answer(i18n.t("admin_menu", lang))

async def cmd_admin_users(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    session = get_session()
    users = session.query(User).all()
    session.close()
    text = "Пользователи:\n"
    for u in users:
        text += f"ID: {u.id}, Name: {u.name}, Role: {u.role}, Lang: {u.language}\n"
    await message.answer(text)

async def cmd_admin_orders(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    session = get_session()
    count_all = session.query(Order).count()
    count_done = session.query(Order).filter(Order.status=="done").count()
    session.close()
    text = f"Всего заказов: {count_all}\nВыполнено: {count_done}"
    await message.answer(text)

async def cmd_admin_reviews(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    session = get_session()
    reviews = session.query(Review).all()
    session.close()
    text = "Отзывы:\n"
    for r in reviews:
        text += f"ID: {r.id}, Specialist: {r.specialist_id}, Rating: {r.rating}, Text: {r.text}\n"
    await message.answer(text)

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_admin, commands="admin")
    dp.register_message_handler(cmd_admin_users, commands="users")
    dp.register_message_handler(cmd_admin_orders, commands="orders")
    dp.register_message_handler(cmd_admin_reviews, commands="reviews")
