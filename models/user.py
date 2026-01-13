from typing import Optional, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель пользователя для FastAPI Users (ID типа int).
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        index=True,
        nullable=False,
    )

    full_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    cart: Mapped["Cart"] = relationship(
        "Cart",
        back_populates="user",
        uselist=False,
    )
    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="user",
    )
