from fastapi import FastAPI, HTTPException, Path, Query
from typing import List, Optional
from data import products
from schemas import Product, ProductCreate
from utils import get_next_id


app = FastAPI(
    title="Прибытков Федор Сергеевич — Домашнее задание №31",
    description="REST API для интернет-магазина товаров из вселенной Рика и Морти",
    version="1.0.0"
)
@app.get(
    "/products/{product_id}",
    response_model=Product,
    status_code=200,
    summary="Получить продукт по ID",
    tags=["Products"]
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

@app.get(
    "/products/",
    response_model=List[Product],
    status_code=200,
    summary="Получить все продукты с фильтрацией и сортировкой",
    tags=["Products"]
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
    
    Examples:
        GET /products/?search=плюмбус
        GET /products/?currency=shmeckles&sort_order=desc
        GET /products/?search=робот&currency=credits&sort_order=asc
    """
    
    result = products.copy()
    
    if search:
        search_lower = search.lower()
        result = [
            product for product in result
            if search_lower in product["name"].lower() or
               search_lower in product["description"].lower()
        ]
    
    
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

@app.post(
    "/products/",
    response_model=Product,
    status_code=201,
    summary="Создать новый продукт",
    tags=["Products"]
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
    
    Example:
        {
            "name": "Волшебный вантуз Рика",
            "description": "Устраняет любые засоры...",
            "prices": {"shmeckles": 45.99, "credits": 33.5},
            "image_url": "/images/rick-plunger.webp"
        }
    """
    new_id = get_next_id()
    
    new_product = {
        "id": new_id,
        **product_data.model_dump()
    }
    
    products.append(new_product)
    
    return new_product

@app.put(
    "/products/{product_id}",
    response_model=Product,
    status_code=200,
    summary="Обновить продукт",
    tags=["Products"]
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
    
    Example:
        PUT /products/1
        Body: {
            "name": "Новое название",
            "description": "Новое описание...",
            "prices": {...},
            "image_url": "..."
        }
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

@app.delete(
    "/products/{product_id}",
    status_code=204,
    summary="Удалить продукт",
    tags=["Products"]
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
    
    Example:
        DELETE /products/1
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
