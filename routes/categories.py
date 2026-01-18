from typing import List
from fastapi import APIRouter, HTTPException, Path, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_async_session
from models.category import Category as CategoryModel
from schemas.category import CategoryCreate, CategoryRead

router = APIRouter(
    prefix="/categories",
    tags=["Категории"],
)

@router.post(
    "/",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать категорию",
)
async def create_category(
    category_data: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    # Проверяем уникальность имени
    stmt = select(CategoryModel).where(
        CategoryModel.name == category_data.name
    )
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Категория с таким именем уже существует",
        )
    
    category = CategoryModel(**category_data.model_dump())
    session.add(category)
    await session.commit()
    await session.refresh(category)
    
    return category

@router.get(
    "/",
    response_model=List[CategoryRead],
    summary="Получить список категорий",
)
async def get_categories(
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(CategoryModel).order_by(CategoryModel.id)
    result = await session.execute(stmt)
    categories = result.scalars().all()
    return categories

@router.get(
    "/{category_id}",
    response_model=CategoryRead,
    summary="Получить категорию по ID",
)
async def get_category(
    category_id: int = Path(..., ge=1, description="ID категории"),
    session: AsyncSession = Depends(get_async_session),
):
    category = await session.get(CategoryModel, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category

@router.put(
    "/{category_id}",
    response_model=CategoryRead,
    summary="Обновить категорию",
)
async def update_category(
    category_id: int,
    category_data: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    category = await session.get(CategoryModel, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    category.name = category_data.name
    await session.commit()
    await session.refresh(category)
    return category

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить категорию",
)
async def delete_category(
    category_id: int = Path(..., ge=1, description="ID категории"),
    session: AsyncSession = Depends(get_async_session),
):
    category = await session.get(CategoryModel, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    await session.delete(category)
    await session.commit()
