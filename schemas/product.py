from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from schemas.category import CategoryRead


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

    image_url: Optional[str] = Field(
        None,
        description="Путь к изображению товара",
        example="/uploads/products/plumbus.webp",
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
