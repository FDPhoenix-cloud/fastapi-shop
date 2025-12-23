from pydantic import BaseModel, Field
from typing import Dict
from schemas.category import CategoryRead
from pydantic import ConfigDict


class Product(BaseModel):
    id: int

    name: str = Field(
        ...,
        description="Название товара",
        example="Стандартный Плюмбус",
    )

    description: str = Field(
        ...,
        description="Детальное описание товара",
        example="Каждый дом должен иметь плюмбус...",
    )

    image_url: str = Field(
        ...,
        description="Путь к изображению товара",
        example="/images/plumbus.webp",
    )

    price_shmeckles: float = Field(
        ...,
        description="Цена в шмекелях",
        example=6.5,
    )

    price_flurbos: float = Field(
        ...,
        description="Цена в флурбо",
        example=3.2,
    )

    price_credits: float = Field(
        ...,
        description="Цена в кредитах",
        example=4.8,
    )
    category: CategoryRead

    model_config = ConfigDict(from_attributes=True)

