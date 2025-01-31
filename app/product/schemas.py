from pydantic import BaseModel, Field


class NewProduct(BaseModel):
    name: str = Field(..., max_length=50, description="Название товара")
    price: float = Field(..., description="Цена товара")


class Product(NewProduct):
    id: int


class ProductList(BaseModel):
    items: list[Product]


class Cart(BaseModel):
    items: list[Product]


class AddProductToCart(BaseModel):
    product_id: int
