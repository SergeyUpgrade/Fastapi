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


    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

