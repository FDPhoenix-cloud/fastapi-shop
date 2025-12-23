from pydantic import BaseModel, Field
from pydantic import ConfigDict


class CategoryCreate(BaseModel):
    """
    Схема создания категории.
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Название категории",
        example="Инструменты Морти",
    )


class CategoryRead(BaseModel):
    """
    Схема чтения категории (ответ API).
    """
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
