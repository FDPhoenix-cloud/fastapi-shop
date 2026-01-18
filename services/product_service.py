# services/product_service.py
from typing import Optional, List

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.product import Product as ProductModel
from models.category import Category as CategoryModel
from schemas import ProductCreate  # или from schemas.product import ProductCreate


async def get_all_products_service(
    session: AsyncSession,
    search: Optional[str] = None,
    currency: Optional[str] = None,
    sort_order: Optional[str] = None,
) -> List[ProductModel]:
    query = select(ProductModel).options(selectinload(ProductModel.category))

    if search:
        like = f"%{search}%"
        query = query.where(
            or_(
                ProductModel.name.ilike(like),
                ProductModel.description.ilike(like),
            )
        )

    if currency and sort_order:
        if currency not in ("shmeckles", "flurbos", "credits"):
            raise ValueError("currency должен быть shmeckles, flurbos или credits")

        if sort_order not in ("asc", "desc"):
            raise ValueError("sort_order должен быть asc или desc")

        column = getattr(ProductModel, f"price_{currency}")
        if sort_order == "desc":
            column = column.desc()
        query = query.order_by(column)

    result = await session.execute(query)
    return result.scalars().all()


async def get_product_by_id_service(
    session: AsyncSession,
    product_id: int,
) -> Optional[ProductModel]:
    query = (
        select(ProductModel)
        .options(selectinload(ProductModel.category))
        .where(ProductModel.id == product_id)
    )
    result = await session.execute(query)
    return result.scalars().first()


async def create_product_service(
    session: AsyncSession,
    product_data: ProductCreate,
) -> ProductModel:
    category = await session.get(CategoryModel, product_data.category_id)
    if category is None:
        raise ValueError("Категория не найдена")

    new_product = ProductModel(**product_data.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)

    query = (
        select(ProductModel)
        .options(selectinload(ProductModel.category))
        .where(ProductModel.id == new_product.id)
    )
    result = await session.execute(query)
    return result.scalars().first()


async def update_product_service(
    session: AsyncSession,
    product_id: int,
    product_data: ProductCreate,
) -> ProductModel:
    product = await session.get(ProductModel, product_id)
    if product is None:
        raise ValueError("Продукт не найден")

    data = product_data.model_dump()

    new_category_id = data.get("category_id")
    if new_category_id is not None:
        category = await session.get(CategoryModel, new_category_id)
        if category is None:
            raise ValueError("Категория не найдена")

    for field, value in data.items():
        setattr(product, field, value)

    await session.commit()
    await session.refresh(product)

    query = (
        select(ProductModel)
        .options(selectinload(ProductModel.category))
        .where(ProductModel.id == product_id)
    )
    result = await session.execute(query)
    return result.scalars().first()


async def delete_product_service(
    session: AsyncSession,
    product_id: int,
) -> None:
    product = await session.get(ProductModel, product_id)
    if product is None:
        raise ValueError("Продукт не найден")

    await session.delete(product)
    await session.commit()
