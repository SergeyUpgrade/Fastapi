#from http.client import HTTPException
#
#from fastapi import Depends, APIRouter
#from sqlalchemy.ext.asyncio import AsyncSession
#from starlette import status
#
#from app.Product.models import Product
#
from fastapi import APIRouter, Body
from . import services
from .models import Product as ProductModel
from .schemas import ProductList, Product, NewProduct
from ..database import async_session_maker, SessionDep

router = APIRouter(prefix='/products', tags=['Products'])


#
#@router.post("/products/", response_model=Product)
#async def create_product(*, db: AsyncSession = Depends(get_db), product: Product):
#    db_obj = Product(**product.dict(exclude_unset=True))
#    db.add(db_obj)
#    await db.commit()
#    return product
#
#@router.put("/products/{id}", response_model=Product)
#async def update_product(*, db: AsyncSession = Depends(get_db), id: int, product: Product):
#    db_obj = await db.execute(Product.__table__.select().where(Product.c.id == id)
#    if not db_obj:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} does not exist")
#    for key, value in product.dict(exclude_unset=True):
#        setattr(db_obj, key, value)
#    db_obj.updated_at = datetime.utcnow()
#    db.commit()
#    return db_obj
#
#@router.delete("/products/{id}")
#async def delete_product(*, db: AsyncSession = Depends(get_db), id: int):
#    db_obj = await db.execute(Product.__table__.select().where(Product.c.id == id)
#    if not db_obj:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} does not exist")
#    db.delete(db_obj)
#    await db.commit()
#    return {"message": f"Product with id {id} was deleted."}

@router.get('/', response_model=ProductList)
async def get_products():
    async with async_session_maker() as session:
        return await services.get_products(session)


@router.get('/{product_id}', response_model=Product)
async def get_products(product_id, session: SessionDep):
    return await services.get_product(session, product_id=product_id)


@router.post('/create', response_model=Product)
async def create_product(product: NewProduct, session: SessionDep):
    return await services.create_product(session, product)


@router.delete('/{product_id}')
async def get_products(product_id: int, session: SessionDep):
    return await services.delete_product(session, product_id=product_id)

@router.post('/{product_id}',response_model=Product)
async def update_products(product: Product, session: SessionDep):
    return await services.update_product(session, product)
