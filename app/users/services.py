from passlib.context import CryptContext
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def __get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(session: AsyncSession, name: str, phone_number: str, email: str, is_admin: bool, password: str):
    user = User(
        name=name,
        phone_number=phone_number,
        email=email,
        is_admin=is_admin,
        password=__get_password_hash(password)
    )
    session.add(user)
    await session.flush()
    return user.id


async def login_user(session: AsyncSession, phone_number: str, email: str, password: str) -> User | None:
    if phone_number:
        result = await session.scalars(select(User).filter(User.phone_number == phone_number))
    elif email:
        result = await session.scalars(select(User).filter(User.email == email))
    else:
        raise ValueError('Укажите телефон или емейл пользователя')
    user = result.one_or_none()
    if user is None:
        return None
    if not pwd_context.verify(password, user.password):
        return None
    return user


async def get_user_role(session: AsyncSession, user_id: int):
    user = await get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise ValueError(f'Пользователя {user_id} не существует')
    if user.is_admin:
        return 'admin'
    return 'customer'


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.scalars(select(User).filter(User.id == user_id))
    return result.one_or_none()


async def is_user_already_exist(session: AsyncSession, phone_number: str, email: str) -> bool:
    result = await session.scalars(select(User).filter(User.email == email))
    if result.one_or_none() is not None:
        return True
    result = await session.scalars(select(User).filter(User.phone_number == phone_number))
    if result.one_or_none() is not None:
        return True
    return False

async def change_user_name(session: AsyncSession, user_id: int, new_name: str) -> None:
    #user = await get_user_by_id(session=session, user_id=user_id)
    #if user is None:
    #    raise ValueError(f"Пользователь с индентификатором {user_id} не найден")
    #print(type(user))
    #user.name = new_name
    #await session.flush()
    await session.execute(update(User).filter(User.id == user_id).values(name=new_name))
    await session.flush()


async def delete_user(session: AsyncSession, user_id: int) -> None:
    user = await get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise ValueError(f"Пользователь с индентификатором {user_id} не найден")
    await session.delete(user)
    await session.flush()
