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
    prices: Dict[str, float] = Field(
        ...,
        description="Цены в разных валютах",
        example={"shmeckles": 45.99, "credits": 33.5, "flurbos": 22.8}
    )
    image_url: str = Field(
        ...,
        description="Путь к изображению товара",
        example="/images/rick-plunger.webp"
    )
