from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field, computed_field


class CartItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(default=1, ge=1)


class ProductInCart(BaseModel):
    id: int
    name: str
    price_shmeckles: float
    price_flurbos: float
    image_url: str | None = None
    quantity: int  # остаток на складе!

    model_config = ConfigDict(from_attributes=True)


class CartItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductInCart

    model_config = ConfigDict(from_attributes=True)


class CartRead(BaseModel):
    id: int
    user_id: int
    items: List[CartItemRead]

    @computed_field
    @property
    def total_price(self) -> float:
        return sum(
            item.product.price_shmeckles * item.quantity
            for item in self.items
        )

    model_config = ConfigDict(from_attributes=True)



class OrderCreate(BaseModel):
    delivery_address: str = Field(min_length=10, max_length=500)
    phone: str = Field(min_length=10, max_length=20)


class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    frozen_name: str
    frozen_price: float

    model_config = ConfigDict(from_attributes=True)


class OrderRead(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    status: str
    total_amount: float
    delivery_address: str
    phone: str
    items: List[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)
