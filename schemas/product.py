from pydantic import BaseModel, Field
from typing import Dict

class Product(BaseModel):
    id: int
    name: str = Field(
        description="Название товара",
        example="Стандартный Плюмбус"
    )
    description: str = Field(
        description="Детальное описание товара",
        example="Каждый дом должен иметь плюмбус..."
    )
    prices: Dict[str, float] = Field(
        description="Цены в разных валютах",
        example={"shmeckles": 6.5, "credits": 4.8, "flurbos": 3.2}
    )
    image_url: str = Field(
        description="Путь к изображению товара",
        example="/images/plumbus.webp"
    )
