#from sqlalchemy import ForeignKey, text, Text
#from sqlalchemy.orm import relationship, Mapped, mapped_column
#from app.database import Base, str_uniq, int_pk, str_null_true
#from datetime import date
#
#class Product(Base):
#    id: Mapped[int_pk]
#    name: Mapped[str]
#    price: Mapped[int]
#    is_active: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
#
#    extend_existing = True
#
#    def __repr__(self):
#        return f"{self.__class__.__name__}(id={self.id})"
#