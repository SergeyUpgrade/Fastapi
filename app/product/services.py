from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker
from app.product.schemas import ProductList, Product, NewProduct
from app.product import models as m


async def get_product(session: AsyncSession, product_id):
    result = await session.execute(select(m.Product).filter(m.Product.id == product_id))
    return result.scalars().all()


async def get_products(session: AsyncSession):
    items: list[Product] = []
    return ProductList(items=items)


async def get_user_cart(user_id):
    pass


async def add_product_to_cart(user_id, product_id):
    cart = get_user_cart(user_id)
    product = get_product(product_id)
    cart.add(product)


async def create_product(session: AsyncSession, product: NewProduct):
    m_product = m.Product(name=product.name, price=product.price)
    session.add(m_product)
    await session.flush()
    return Product(name=m_product.name, price=m_product.price, id=m_product.id)


async def delete_product(session: AsyncSession, product_id: int):
    await session.execute(delete(m.Product).filter(m.Product.id == product_id))
    await session.flush()
    return f'Успешно удалено'

async def update_product(session: AsyncSession, product: Product):
    await session.execute(update(m.Product).filter(m.Product.id == product.id).values(name=product.name, price=product.price))
    await session.flush()
    return product
