from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from . import services as ss
from . import schemas as sm
from . import presentations as sp
from ..database import SessionDep
from ..users.auth import get_current_user_id
from ..users import services as users_services

router = APIRouter(prefix='/products', tags=['Products'])


@router.get('/')
async def products(session: SessionDep, user_id: int = Depends(get_current_user_id)):
    is_admin = await __is_user_admin(session=session, user_id=user_id)
    return await sp.show_products(session=session, is_admin=is_admin)

@router.post('/product/create')
async def create_product(new_product: sm.NewProduct, session: SessionDep, user_id: int = Depends(get_current_user_id)):
    await __required_admin_role(session=session, user_id=user_id)
    product_id = await ss.create_product(
        name=new_product.name,
        price=new_product.price,
        is_active=True,
        session=session
    )
    return {'product_id': product_id}

@router.delete('/product/{product_id}')
async def get_products(product_id: int, session: SessionDep, user_id: int = Depends(get_current_user_id)):
    await __required_admin_role(session=session, user_id=user_id)
    await ss.delete_product(session, product_id=product_id)
    return {'message': 'Продукт удален'}


@router.post('/product/{product_id}')
async def update_products(product: sm.Product, session: SessionDep, user_id: int = Depends(get_current_user_id)):
    await __required_admin_role(session=session, user_id=user_id)
    await ss.update_product(session, product_id=product.id, name=product.name, price=product.price)
    return {'message': 'Продукт обновлен'}

@router.get('/cart')
async def get_user_cart(session: SessionDep, user_id: int = Depends(get_current_user_id)):
    print(user_id)
    return await sp.show_cart(session=session, user_id=user_id)


@router.post('/cart/add_item')
async def add_item_to_cart(session: SessionDep, product_id: int, user_id: int = Depends(get_current_user_id)):
    cart = await ss.get_or_create_cart(session=session, user_id=user_id)
    await ss.create_cart_item(
        session=session,
        cart_id=cart.id,
        product_id=product_id
    )
    return {'message': f'Продукт {product_id} успешно добавлен'}

@router.delete('/cart/delete_item')
async def add_item_to_cart(session: SessionDep, product_id: int, user_id: int = Depends(get_current_user_id)):
    cart = await ss.get_or_create_cart(session=session, user_id=user_id)
    await ss.delete_product_from_cart(
        session=session,
        cart_id=cart.id,
        product_id=product_id
    )
    return {'message': f'Продукт {product_id} успешно удален'}

@router.post('/cart/delete_all_item')
async def add_item_to_cart(session: SessionDep, user_id: int = Depends(get_current_user_id)):
    cart = await ss.get_or_create_cart(session=session, user_id=user_id)
    await ss.delete_all_products_from_cart(
        session=session,
        cart_id=cart.id
    )
    return {'message': f'Корзина очищена'}


async def __required_admin_role(session, user_id: int):
    role = await users_services.get_user_role(session=session, user_id=user_id)
    if role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


async def __is_user_admin(session, user_id: int):
    role = await users_services.get_user_role(session=session, user_id=user_id)
    return role == 'admin'