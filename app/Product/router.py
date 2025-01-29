from http.client import HTTPException

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.Product.models import Product

router = APIRouter(prefix='/products', tags=['Products'])

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