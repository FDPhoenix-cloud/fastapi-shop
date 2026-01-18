from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base
from core.config import settings

# Base для моделей
Base = declarative_base()

# Создаём движок (ОДИН на всё приложение!)
engine = create_async_engine(
    settings.database_url,
    echo=True,  # выключить в продакшене
    future=True,
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """Инициализирует БД (создаёт все таблицы)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
