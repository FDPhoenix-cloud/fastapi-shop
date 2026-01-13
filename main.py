import logging
from auth import auth_router
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import Dict
from core.config import settings
from core.database import init_db
from routes.products import router as products_router
from routes.categories import router as categories_router
from routes.cart import router as cart_router
from routes.orders import router as orders_router


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Код старта и остановки приложения.
    """
    print("База данных инициализирована")
    yield
    print("Приложение остановлено")


app = FastAPI(
    title="Прибытков Федор Сергеевич — ДЗ №35",
    description="REST API магазина с БД (SQLAlchemy 2.0)",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(products_router)
app.include_router(categories_router)
app.include_router(auth_router)
app.include_router(cart_router, prefix="/cart", tags=["Cart"])     
app.include_router(orders_router, prefix="/orders", tags=["Orders"])

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

logger.info("✅ Статические файлы (uploads) подключены")



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
