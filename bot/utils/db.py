# bot/utils/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.utils.config_reader import config
from bot.utils.logger import logger
from bot.models import Base, User, Order, Review  # Импорт моделей

# Настройка подключения к базе данных
engine = create_engine(config.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# Создание всех таблиц (если они ещё не созданы)
Base.metadata.create_all(bind=engine)

# Функция для получения пользователя по telegram_id
def get_user(telegram_id: int):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        return user
    except Exception as e:
        logger.error(f"Ошибка при получении пользователя: {e}")
        return None
    finally:
        session.close()

# Функция для создания нового пользователя
def create_user(telegram_id: int, name: str, city: str, contact: str, role: str,
               service_category: str = None, experience: str = None,
               region: str = None, language: str = "ru"):
    session = SessionLocal()
    try:
        new_user = User(
            telegram_id=telegram_id,
            name=name,
            city=city,
            contact=contact,
            role=role,
            service_category=service_category,
            experience=experience,
            region=region,
            language=language
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        logger.info(f"Пользователь создан: {new_user}")
        return new_user  # Возвращаем объект пользователя
    except Exception as e:
        session.rollback()
        logger.error(f"Ошибка при создании пользователя: {e}")
        return None
    finally:
        session.close()

# Функция для получения специалистов по категории
def get_specialists_by_category(category: str):
    """
    Возвращает список специалистов по заданной категории услуг.
    """
    session = SessionLocal()
    try:
        specialists = session.query(User).filter(
            User.role == "specialist",
            User.service_category.ilike(f"%{category}%")
        ).all()
        return specialists
    except Exception as e:
        logger.error(f"Ошибка при получении специалистов по категории '{category}': {e}")
        return []
    finally:
        session.close()

# Функция для создания нового заказа
def create_order(user_id: int, description: str, category: str = None,
                preferred_time: str = None, location: str = None, status: str = "open"):
    session = SessionLocal()
    try:
        new_order = Order(
            user_id=user_id,
            description=description,
            category=category,
            preferred_time=preferred_time,
            location=location,
            status=status
        )
        session.add(new_order)
        session.commit()
        session.refresh(new_order)
        logger.info(f"Заказ создан: {new_order}")
        return new_order  # Возвращаем объект заказа
    except Exception as e:
        session.rollback()
        logger.error(f"Ошибка при создании заказа: {e}")
        return None
    finally:
        session.close()

# Функция для получения заказов пользователя
def get_orders(user_id: int):
    session = SessionLocal()
    try:
        orders = session.query(Order).filter(Order.user_id == user_id).all()
        return orders
    except Exception as e:
        logger.error(f"Ошибка при получении заказов пользователя {user_id}: {e}")
        return []
    finally:
        session.close()

# Функция для создания отзыва
def create_review(specialist_id: int, user_id: int, rating: float, text: str = None):
    session = SessionLocal()
    try:
        new_review = Review(
            specialist_id=specialist_id,
            user_id=user_id,
            rating=rating,
            text=text
        )
        session.add(new_review)
        session.commit()
        session.refresh(new_review)
        logger.info(f"Отзыв создан: {new_review}")
        return new_review
    except Exception as e:
        session.rollback()
        logger.error(f"Ошибка при создании отзыва: {e}")
        return None
    finally:
        session.close()

# Функция для получения отзывов специалиста
def get_reviews_for_specialist(specialist_id: int):
    session = SessionLocal()
    try:
        reviews = session.query(Review).filter(Review.specialist_id == specialist_id).all()
        return reviews
    except Exception as e:
        logger.error(f"Ошибка при получении отзывов для специалиста {specialist_id}: {e}")
        return []
    finally:
        session.close()


def update_user():
    return None