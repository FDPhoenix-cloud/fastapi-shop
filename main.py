from fastapi import FastAPI
from typing import List
from data import products
from schemas.product import Product

# Создание экземпляра FastAPI с параметрами документации
app = FastAPI(
    title="Прибытков Федор Сергеевич — Домашнее задание №31",
    description="REST API для интернет-магазина товаров из вселенной Рика и Морти",
    version="1.0.0"
)

# Создание GET-эндпоинта для получения всех продуктов
@app.get(
    "/products/",
    response_model=List[Product],
    status_code=200,
    summary="Получить все продукты",
    tags=["Products"]
)
async def get_all_products():
    """
    Получить список всех доступных продуктов.
    
    Возвращает список из 20 товаров с информацией:
    - id: уникальный идентификатор товара
    - name: название товара
    - description: подробное описание
    - prices: цены в разных валютах
    - image_url: ссылка на изображение товара
    """
    return products
