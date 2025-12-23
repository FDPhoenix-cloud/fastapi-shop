from pydantic import BaseModel, Field
from typing import Dict

class ProductCreate(BaseModel):
    """
    Pydantic модель для создания и обновления продукта.
    Не включает поле 'id', так как оно генерируется автоматически.
    """
    name: str = Field(
        ...,
        min_length=1,
        description="Название товара",
        example="Волшебный вантуз Рика"
    )
    description: str = Field(
        ...,
        min_length=5,
        description="Детальное описание товара",
        example="Устраняет любые засоры в пространственно-временном континууме"
    )
    price_shmeckles: float = Field(
        ...,
        gt=0,
        description="Цена в шмекелях",
        example=6.5,
    )
    price_flurbos: float = Field(
        ...,
        gt=0,
        description="Цена в флурбо",
        example=3.2,
    )
    price_credits: float = Field(
        ...,
        gt=0,
        description="Цена в кредитах",
        example=4.8,
    )
    image_url: str = Field(
        ...,
        description="Путь к изображению товара",
        example="/images/rick-plunger.webp"
    )
    category_id: int = Field(
        ...,
        ge=1,
        description="ID категории, к которой относится товар",
        example=1,
    )
