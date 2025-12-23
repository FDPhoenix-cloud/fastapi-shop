from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings
from models.base import Base
from models.product import Product  # noqa: F401
from models.category import Category

# URL подключения к БД
DATABASE_URL = settings.database_url

# Движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
