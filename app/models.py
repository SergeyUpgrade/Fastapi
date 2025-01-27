from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date


# создаем модель таблицы студентов
class Users(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    name: Mapped[str]
    email: Mapped[str_uniq]
    password: Mapped[str]
