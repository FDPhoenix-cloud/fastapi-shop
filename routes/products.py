from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional

from schemas import Product, ProductCreate
from data.products import products
from utils.helpers import get_next_id

# Создаём роутер для продуктов
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# ==================== GET /products/ ====================
@router.get(
    "/",
    response_model=List[Product],
    status_code=200,
    summary="Получить все продукты с фильтрацией и сортировкой"
)
async def get_all_products(
    search: Optional[str] = Query(
        None,
        description="Поиск по названию или описанию продукта"
    ),
    currency: Optional[str] = Query(
        None,
        description="Валюта для сортировки (shmeckles, credits, flurbos)"
    ),
    sort_order: Optional[str] = Query(
        None,
        description="Направление сортировки (asc - возрастание, desc - убывание)"
    )
):
    """
    Получить список всех продуктов с возможностью фильтрации и сортировки.
    
    Query параметры:
        - search: Строка для поиска в названии и описании (регистронезависимый)
        - currency: Валюта для сортировки по цене
        - sort_order: Направление сортировки (asc или desc)
    
    Returns:
        List[Product]: Список продуктов, отфильтрованный и отсортированный
    """
    result = products.copy()
    
    # ФИЛЬТРАЦИЯ по поиску
    if search:
        search_lower = search.lower()
        result = [
            product for product in result
            if search_lower in product["name"].lower() or
               search_lower in product["description"].lower()
        ]
    
    # СОРТИРОВКА по валюте
    if currency and sort_order:
        if sort_order not in ["asc", "desc"]:
            raise HTTPException(
                status_code=400,
                detail="sort_order должен быть 'asc' или 'desc'"
            )
        
        result = [
            product for product in result
            if currency in product.get("prices", {})
        ]
        
        result.sort(
            key=lambda p: p["prices"][currency],
            reverse=(sort_order == "desc")
        )
    
    return result


# ==================== GET /products/{product_id} ====================
@router.get(
    "/{product_id}",
    response_model=Product,
    status_code=200,
    summary="Получить продукт по ID"
)
async def get_product(
    product_id: int = Path(..., ge=1, description="ID продукта")
):
    """
    Получить информацию о конкретном продукте по его ID.
    
    Args:
        product_id: Уникальный идентификатор продукта (должен быть >= 1)
    
    Returns:
        Product: Объект продукта с полной информацией
    
    Raises:
        HTTPException: Если продукт с таким ID не найден (404)
    """
    for product in products:
        if product["id"] == product_id:
            return product
    
    raise HTTPException(
        status_code=404,
        detail="Продукт не найден"
    )


# ==================== POST /products/ ====================
@router.post(
    "/",
    response_model=Product,
    status_code=201,
    summary="Создать новый продукт"
)
async def create_product(product_data: ProductCreate):
    """
    Создать новый продукт в каталоге.
    
    Body:
        product_data: Данные нового продукта (без ID)
    
    Returns:
        Product: Созданный продукт с автоматически сгенерированным ID
    
    Status Code:
        201: Продукт успешно создан
    """
    new_id = get_next_id()
    
    new_product = {
        "id": new_id,
        **product_data.model_dump()
    }
    
    products.append(new_product)
    
    return new_product


# ==================== PUT /products/{product_id} ====================
@router.put(
    "/{product_id}",
    response_model=Product,
    status_code=200,
    summary="Обновить продукт"
)
async def update_product(
    product_id: int = Path(..., ge=1, description="ID продукта"),
    product_data: ProductCreate = None
):
    """
    Обновить информацию о существующем продукте.
    
    Args:
        product_id: ID продукта для обновления
        product_data: Новые данные продукта
    
    Returns:
        Product: Обновленный продукт
    
    Raises:
        HTTPException: Если продукт не найден (404)
    
    Status Code:
        200: Продукт успешно обновлен
    """
    product_index = None
    for idx, product in enumerate(products):
        if product["id"] == product_id:
            product_index = idx
            break
    
    if product_index is None:
        raise HTTPException(
            status_code=404,
            detail="Продукт не найден"
        )
    
    updated_product = {
        "id": product_id,
        **product_data.model_dump()
    }
    
    products[product_index] = updated_product
    
    return updated_product


# ==================== DELETE /products/{product_id} ====================
@router.delete(
    "/{product_id}",
    status_code=204,
    summary="Удалить продукт"
)
async def delete_product(
    product_id: int = Path(..., ge=1, description="ID продукта")
):
    """
    Удалить продукт из каталога.
    
    Args:
        product_id: ID продукта для удаления
    
    Raises:
        HTTPException: Если продукт не найден (404)
    
    Status Code:
        204: Продукт успешно удален (без содержимого в ответе)
    """
    product_index = None
    for idx, product in enumerate(products):
        if product["id"] == product_id:
            product_index = idx
            break
    
    if product_index is None:
        raise HTTPException(
            status_code=404,
            detail="Продукт не найден"
        )
    
    products.pop(product_index)
    
    return None
