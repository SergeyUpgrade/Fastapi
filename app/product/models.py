from sqlalchemy import ForeignKey, text, Text, Integer, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date


class Product(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    price: Mapped[int]
    cart_id = Column(Integer, ForeignKey('cart.id'))

    cart = relationship("Cart", back_populates="products")
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class Cart(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
    )

    @property
    def user(self):
        from app.users.models import Users
        return relationship(Users, back_populates='cart')

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="cart",
        cascade="all, delete",
    )


class CartItem(Base):
    id: Mapped[int_pk]
    product_id: Mapped[int] = mapped_column(
        Integer
    )
    cart_id: Mapped[int] = mapped_column(
        Integer
    )
    user_id: Mapped[int] = mapped_column(
        Integer
    )