from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker
from app.product.schemas import ProductList, Product, NewProduct, Cart
from app.product import models as m


async def get_product(session: AsyncSession, product_id):
    result = await session.execute(select(m.Product).filter(m.Product.id == product_id))
    return result.scalars().all()


async def get_products(session: AsyncSession):
    items: list[Product] = []
    return ProductList(items=items)


async def get_user_cart(user_id, session: AsyncSession):
    cart = Cart(items=[])
    m_cart = await __get_or_create_cart(user_id, session)
    m_cart_items = await __get_cart_items(m_cart.id, session)
    return cart


async def add_item_to_cart(user_id, product_id, session: AsyncSession):
    m_cart = await __get_or_create_cart(user_id, session)
    m_product = await __get_product(product_id, session)
    if m_product is None:
        return f"Нет такого продукта"
    m_cartitem = m.CartItem(product_id=product_id, cart_id=m_cart.id)
    session.add(m_cartitem)
    await session.flush()
    return f'Продукт добавлен'


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

async def __get_or_create_cart(user_id, session: AsyncSession):
    result = await session.scalars(select(m.Cart).filter(m.Cart.user_id == user_id))
    m_cart = result.one_or_none()
    print(m_cart)
    if m_cart is None:
        m_cart = m.Cart(user_id=user_id)
        session.add(m_cart)
        await session.flush()
    return m_cart

async def __get_cart_items(cart_id, session: AsyncSession):
    result = await session.execute(select(m.CartItem).filter(m.CartItem.cart_id == cart_id))
    m_cart_items = result.all()
    return m_cart_items


async def __get_product(product_id, session: AsyncSession):
    result = await session.scalars(select(m.Product).filter(m.Product.id == product_id))
    m_product = result.one_or_none()
    print(m_product)
    return m_product