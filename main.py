import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from pathlib import Path

from core.database import engine, Base
from core.config import settings
from routes.products import router as products_router
from routes.categories import router as categories_router
from routes.cart import router as cart_router
from routes.orders import router as orders_router
from auth import auth_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация и завершение приложения"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Все таблицы созданы!")
    yield
    logger.info("🛑 Приложение остановлено")


app = FastAPI(
    title="API Магазина - ДЗ №42",
    description="FastAPI + SQLAlchemy интернет-магазин",
    version="1.0.0",
    lifespan=lifespan,
)

# ✅ CORS CONFIGURATION - ИСПРАВЛЕНО!
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(products_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(auth_router)

images_dir = Path("images")
if images_dir.exists():
    app.mount("/images", StaticFiles(directory="images"), name="images")

# Статические файлы
try:
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
    logger.info("✅ Статические файлы подключены")
except Exception as e:
    logger.warning(f"⚠️ Не удалось подключить статические файлы: {e}")


@app.get("/")
async def root() -> Dict[str, str]:
    """Корневой эндпоинт"""
    return {
        "message": "🚀 Добро пожаловать в API магазина!",
        "docs": "/docs",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)