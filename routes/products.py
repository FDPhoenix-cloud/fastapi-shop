from fastapi import APIRouter, HTTPException, Path, Query, BackgroundTasks
from typing import List, Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import Product, ProductCreate
from core.database import AsyncSessionLocal
from models.product import Product as ProductModel
from utils.telegram import send_telegram_message

from models.category import Category as CategoryModel
from sqlalchemy.orm import selectinload



# Создаём роутер для продуктов
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# ==================== GET /products/ ====================
@router.get(
    "/",
    response_model=List[Product],
    summary="Получить все продукты (из БД)",
)
async def get_all_products(
    search: Optional[str] = Query(
        None,
        description="Поиск по названию или описанию",
    ),
    currency: Optional[str] = Query(
        None,
        description="Валюта для сортировки (shmeckles, flurbos, credits)",
    ),
    sort_order: Optional[str] = Query(
        None,
        description="Направление сортировки (asc или desc)",
    ),
):
    async with AsyncSessionLocal() as session:  # type: AsyncSession
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
                raise HTTPException(
                    status_code=400,
                    detail="currency должен быть shmeckles, flurbos или credits",
                )
            if sort_order not in ("asc", "desc"):
                raise HTTPException(
                    status_code=400,
                    detail="sort_order должен быть asc или desc",
                )

            column = getattr(ProductModel, f"price_{currency}")
            if sort_order == "desc":
                column = column.desc()
            query = query.order_by(column)

        result = await session.execute(query)
        products = result.scalars().all()
        return products



# ==================== GET /products/{product_id} ====================
@router.get(
    "/{product_id}",
    response_model=Product,
    summary="Получить продукт по ID",
)
async def get_product(
    product_id: int = Path(..., ge=1, description="ID продукта"),
):
    async with AsyncSessionLocal() as session:
        query = (
            select(ProductModel)
            .options(selectinload(ProductModel.category))
            .where(ProductModel.id == product_id)
        )
        result = await session.execute(query)
        product = result.scalars().first()
        if product is None:
            raise HTTPException(status_code=404, detail="Продукт не найден")
        return product




# ==================== POST /products/ ====================
@router.post(
    "/",
    response_model=Product,
    status_code=201,
    summary="Создать продукт",
)
async def create_product(
    product_data: ProductCreate,
    background_tasks: BackgroundTasks,
) -> Product:
    async with AsyncSessionLocal() as session:
        # 1. Проверяем категорию
        category = await session.get(CategoryModel, product_data.category_id)
        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Категория не найдена",
            )

        # 2. Создаём продукт
        new_product = ProductModel(**product_data.model_dump())
        session.add(new_product)
        await session.commit()

        # 3. Получаем продукт заново с жадной загрузкой category
        query = (
            select(ProductModel)
            .options(selectinload(ProductModel.category))
            .where(ProductModel.id == new_product.id)
        )
        result = await session.execute(query)
        new_product = result.scalars().first()

        # 4. Телеграм-уведомление
        if background_tasks is not None and new_product is not None:
            message = f"""🆕 *Создан новый продукт*

📦 *Название:* {new_product.name}
🆔 *ID:* {new_product.id}
📝 *Описание:* {new_product.description[:150]}...

💰 *Цены:*
  • Шмекели: {new_product.price_shmeckles}
  • Флурбо: {new_product.price_flurbos}
  • Кредиты: {new_product.price_credits}

🏷 *Категория:* {new_product.category.name}
"""
            background_tasks.add_task(send_telegram_message, message)

        return new_product





# ==================== PUT /products/{product_id} ====================
@router.put(
    "/{product_id}",
    response_model=Product,
    summary="Обновить продукт",
)
async def update_product(
    product_id: int = Path(..., ge=1, description="ID продукта"),
    product_data: ProductCreate = None,
    background_tasks: BackgroundTasks = None,
) -> Product:
    async with AsyncSessionLocal() as session:
        product = await session.get(ProductModel, product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Продукт не найден")

        if product_data is None:
            raise HTTPException(status_code=400, detail="Нет данных для обновления")

        data = product_data.model_dump()

        # проверяем категорию, если передана
        new_category_id = data.get("category_id")
        if new_category_id is not None:
            category = await session.get(CategoryModel, new_category_id)
            if category is None:
                raise HTTPException(
                    status_code=404,
                    detail="Категория не найдена",
                )

        for field, value in data.items():
            setattr(product, field, value)

        await session.commit()

        query = (
            select(ProductModel)
            .options(selectinload(ProductModel.category))
            .where(ProductModel.id == product_id)
        )
        result = await session.execute(query)
        product = result.scalars().first()

        if background_tasks is not None and product is not None:
            message = f"""🔄 *Обновлён продукт*

📦 *Название:* {product.name}
🆔 *ID:* {product.id}
📝 *Описание:* {product.description[:150]}...

💰 *Цены:*
  • Шмекели: {product.price_shmeckles}
  • Флурбо: {product.price_flurbos}
  • Кредиты: {product.price_credits}

🏷 *Категория:* {product.category.name}
"""
            background_tasks.add_task(send_telegram_message, message)

        return product





# ==================== DELETE /products/{product_id} ====================
@router.delete(
    "/{product_id}",
    status_code=204,
    summary="Удалить продукт",
)
async def delete_product(
    product_id: int = Path(..., ge=1, description="ID продукта"),
):
    async with AsyncSessionLocal() as session:
        product = await session.get(ProductModel, product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Продукт не найден")

        await session.delete(product)
        await session.commit()
        return None

