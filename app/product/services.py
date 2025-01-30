from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker
from app.product.schemas import ProductList, Product
from app.product.models import Product as ProductModel



async def get_product(session: AsyncSession, product_id):
    result = await session.execute(select(ProductModel).filter(ProductModel.id == product_id))
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

def create_product(session: AsyncSession, product: Product):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
