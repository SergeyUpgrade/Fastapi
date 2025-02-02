from datetime import datetime
from typing import Annotated, Type

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, Session, sessionmaker

from app.config import get_db_url

DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


from contextlib import asynccontextmanager


#@asynccontextmanager
#async def get_session():
#    with async_sessionmaker(engine) as session:
#        yield session
#        await session.commit()
async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.commit()

SessionDep = Annotated[Session, Depends(get_session)]

# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

async def db_create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)