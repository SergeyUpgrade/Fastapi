from pydantic import BaseModel

class NewProduct(BaseModel):
    name: str
    price: float


class Product(NewProduct):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class ProductList(BaseModel):
    items: list[Product]


class Cart(BaseModel):
    items: list[Product]


class AddProductToCart(BaseModel):
    product_id: int
