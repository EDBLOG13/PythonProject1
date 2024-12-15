# bot/handlers/reviews.py

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot.utils.db import get_user, create_review  # Исправлен импорт
from bot.utils.i18n import i18n
from bot.states.review_states import ReviewStates  # Импортируем из states
from bot.utils.logger import logger  # Импортируем логгер

async def cmd_leave_review_prompt(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} инициировал оставление отзыва")
    user = get_user(message.from_user.id)
    if not user:
        await message.answer("Пожалуйста, зарегистрируйтесь сначала с помощью /start.")
        logger.warning(f"Неавторизованный пользователь {message.from_user.id} пытается оставить отзыв")
        return

    lang = user.language
    await message.answer(i18n.t("leave_review_for", lang))
    await ReviewStates.specialist_id.set()

async def process_review_specialist_id(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    lang = user.language if user else "ru"
    try:
        # Ожидаем ввод в формате: <ID_специалиста> <оценка(1-5)> <текст>
        parts = message.text.strip().split(' ', 2)
        if len(parts) < 2:
            raise ValueError("Недостаточно данных для отзыва")
        specialist_id = int(parts[0])
        rating = float(parts[1])
        review_text = parts[2] if len(parts) > 2 else ""
        if not (1 <= rating <= 5):
            raise ValueError("Оценка должна быть от 1 до 5")
    except ValueError as e:
        await message.answer("Пожалуйста, введите отзыв в правильном формате: <ID_специалиста> <оценка(1-5)> <текст>")
        logger.error(f"Пользователь {message.from_user.id} ввёл неверный формат отзыва: {message.text}")
        return

    # Проверяем, существует ли специалист с таким ID
    specialist = get_user(specialist_id)
    if not specialist or specialist.role != "specialist":
        await message.answer("Специалист с таким ID не найден.")
        logger.warning(
            f"Пользователь {message.from_user.id} попытался оставить отзыв для несуществующего специалиста ID {specialist_id}")
        return

    # Сохраняем данные в состоянии
    await state.update_data(specialist_id=specialist_id, rating=rating, text=review_text)

    # Добавляем отзыв в базу данных
    review = create_review(
        specialist_id=specialist_id,
        user_id=user.id,
        rating=rating,
        text=review_text
    )
    if review:
        await message.answer(i18n.t("review_submitted", lang))
        logger.info(f"Пользователь {message.from_user.id} оставил отзыв для специалиста ID {specialist_id}")
    else:
        await message.answer(i18n.t("review_creation_failed", lang))  # Убедитесь, что этот ключ существует в переводах
        logger.error(f"Не удалось создать отзыв для специалиста ID {specialist_id} от пользователя {user.id}")

    await state.finish()

def register_reviews_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_leave_review_prompt, commands="leave_review", state="*")
    dp.register_message_handler(process_review_specialist_id, state=ReviewStates.specialist_id)
