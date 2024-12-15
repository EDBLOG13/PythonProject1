# bot/models.py

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "client", "specialist", "admin"
    service_category = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    region = Column(String, nullable=True)
    rating = Column(Float, default=0.0)
    language = Column(String, default="ru")
    blocked = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID клиента, который создал заказ
    description = Column(String, nullable=False)
    category = Column(String, nullable=True)
    preferred_time = Column(String, nullable=True)
    location = Column(String, nullable=True)
    status = Column(String, default="open")  # open, in_progress, done

    user = relationship("User", back_populates="orders")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    specialist_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID специалиста, которому оставили отзыв
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)        # ID пользователя (клиента), который оставил отзыв
    rating = Column(Float, nullable=False)           # Оценка от 1 до 5
    text = Column(String, nullable=True)            # Текст отзыва

    specialist = relationship("User", foreign_keys=[specialist_id], backref="received_reviews")
    user = relationship("User", foreign_keys=[user_id], backref="written_reviews")
