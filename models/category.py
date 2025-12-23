from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Category(Base):
    """
    Категория товара.
    Одна категория может содержать много продуктов.
    """
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    # Обратная связь: список продуктов в этой категории
    products: Mapped[List["Product"]] = relationship(
        back_populates="category",
    )
