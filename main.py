from fastapi import FastAPI
from typing import Dict

# Импорты роутеров
from routes.products import router as products_router

# Импорт конфигурации
from config import settings

# Создаём экземпляр FastAPI
app = FastAPI(
    title="Ваше ФИО — Домашнее задание №33",
    description="Рефакторенный REST API для интернет-магазина товаров из вселенной Рика и Морти",
    version="2.0.0"
)

# ==================== Подключаем роутеры ====================
app.include_router(products_router)


# ==================== Корневой эндпоинт ====================
@app.get("/")
async def root() -> Dict[str, str]:
    """
    Корневой эндпоинт с информацией о приложении.
    
    Демонстрирует работу конфигурации и переменных окружения.
    
    Returns:
        Dict с информацией о приложении
    """
    # Маскируем ключ API (показываем только первые 10 символов)
    masked_key = settings.tg_bot_key[:10] + "..." if len(settings.tg_bot_key) > 10 else settings.tg_bot_key
    
    return {
        "message": "Добро пожаловать в API магазина из вселенной Рика и Морти!",
        "version": "2.0.0 (Рефакторенная версия)",
        "bot_key_sample": masked_key,
        "docs_url": "/docs"
    }


# ==================== Запуск приложения ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
