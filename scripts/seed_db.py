import asyncio
import sys
from pathlib import Path
import os

# Добавляем корень backend в path
backend_path = str(Path(__file__).parent.parent)
sys.path.insert(0, backend_path)
os.chdir(backend_path)

# ⚠️ ВАЖНО: ИМПОРТИРУЕМ ВСЕ МОДЕЛИ ЯВНО ИЗ ПРАВИЛЬНОГО МЕСТА!
from core.database import Base
from models.category import Category
from models.product import Product

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Жестко указываем БД
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Данные товаров - ВСЕ КАРТИНКИ .webp
PRODUCTS = [
    {
        "name": "Каждый дом должен иметь плюшбус",
        "description": "Мы не знаем, что он делает, но он делает это очень хорошо. В комплекте: шлее, грубо и флиб.",
        "price_shmeckles": 1299,
        "price_flurbos": 844,
        "price_credits": 961,
        "image_url": "/images/plumbus.webp",
        "category_id": 1,
    },
    {
        "name": "Нужна помощь по дому?",
        "description": "Нажмите кнопку, и повяется Миксис, готовый выполнить одно ваше поручение.",
        "price_shmeckles": 2499,
        "price_flurbos": 1624,
        "price_credits": 1849,
        "image_url": "/images/meeseeks-box.webp",
        "category_id": 2,
    },
    {
        "name": "Портальная пушка",
        "description": "Заряд портальной жидкости на 37%. Возвратку не подлежит. Может пахнуть приключениями.",
        "price_shmeckles": 9999,
        "price_flurbos": 6499,
        "price_credits": 7399,
        "image_url": "/images/portal-gun.webp",
        "category_id": 1,
    },
    {
        "name": "Темная материя",
        "description": "Идеальное топливо для космического корабля. Всего одна капля позволит улететь.",
        "price_shmeckles": 3599,
        "price_flurbos": 2339,
        "price_credits": 2663,
        "image_url": "/images/dark-matter.webp",
        "category_id": 3,
    },
    {
        "name": "Масло-робот",
        "description": "Его единственная цель существования — передавать масло. Отличный собеседник!",
        "price_shmeckles": 1099,
        "price_flurbos": 714,
        "price_credits": 814,
        "image_url": "/images/butter-robot.webp",
        "category_id": 2,
    },
    {
        "name": "Шлем для чтения мыслей собак",
        "description": "Теперь узнаешь где пес спрятал тапки и почему лает на пылесос!",
        "price_shmeckles": 799,
        "price_flurbos": 519,
        "price_credits": 591,
        "image_url": "/images/dog-helmet.webp",
        "category_id": 1,
    },
    {
        "name": "Глазастые зерновые",
        "description": "Маленькие существа, которые живят в коробке. Очень чувствительны к молоку.",
        "price_shmeckles": 449,
        "price_flurbos": 292,
        "price_credits": 332,
        "image_url": "/images/eyeholes.webp",
        "category_id": 1,
    },
    {
        "name": "Ботинки для ходьбы по стенам",
        "description": "Гравитация — для слабаков! Летай где угодно с этими ботинками.",
        "price_shmeckles": 2099,
        "price_flurbos": 1364,
        "price_credits": 1553,
        "image_url": "/images/gravity-shoes.webp",
        "category_id": 2,
    },
    {
        "name": "Клон-пистолет",
        "description": "Создавай копии. Но помни: копия может растаять через час!",
        "price_shmeckles": 5555,
        "price_flurbos": 3610,
        "price_credits": 4111,
        "image_url": "/images/clone-gun.webp",
        "category_id": 3,
    },
    {
        "name": "Пистолет-уменьшитель",
        "description": "Уменьшает предметы до карманного размера. Идеально для путешествий!",
        "price_shmeckles": 3199,
        "price_flurbos": 2079,
        "price_credits": 2367,
        "image_url": "/images/shrinking-ray.webp",
        "category_id": 3,
    },
    {
        "name": "Крем вечной молодости",
        "description": "Останавливает старение. Необратимо! Побочные эффекты неизвестны.",
        "price_shmeckles": 6799,
        "price_flurbos": 4419,
        "price_credits": 5031,
        "image_url": "/images/age-cream.webp",
        "category_id": 1,
    },
    {
        "name": "Кристалл смерти",
        "description": "Показывает все варианты твоей смерти. Весело и пугающе одновременно!",
        "price_shmeckles": 799,
        "price_flurbos": 519,
        "price_credits": 591,
        "image_url": "/images/death-crystal.webp",
        "category_id": 3,
    },
    {
        "name": "Устройство управления снами",
        "description": "Проникни в сны учителя и заставь поставить пятёрку! Работает как магия!",
        "price_shmeckles": 4099,
        "price_flurbos": 2664,
        "price_credits": 3033,
        "image_url": "/images/dream-inator.webp",
        "category_id": 2,
    },
    {
        "name": "Анатомический парк",
        "description": "Постройте полноценный парк прямо внутри человека. Очень маленький масштаб!",
        "price_shmeckles": 1999,
        "price_flurbos": 1299,
        "price_credits": 1479,
        "image_url": "/images/anatomy-park.webp",
        "category_id": 3,
    },
    {
        "name": "Межвселенское телевидение",
        "description": "Доступ к каналам мультивселенной! Есть ли там спорт? Никто не знает!",
        "price_shmeckles": 4999,
        "price_flurbos": 3249,
        "price_credits": 3699,
        "image_url": "/images/interdimensional-cable.webp",
        "category_id": 1,
    },
    {
        "name": "Симулятор Роя",
        "description": "Проживи жизнь обычного парня. Что может пойти не так?",
        "price_shmeckles": 1299,
        "price_flurbos": 844,
        "price_credits": 961,
        "image_url": "/images/roy-game.webp",
        "category_id": 2,
    },
    {
        "name": "Говорящий кот",
        "description": "Умеет говорить, но лучше не знать о чём. Очень саркастичен.",
        "price_shmeckles": 599,
        "price_flurbos": 389,
        "price_credits": 443,
        "image_url": "/images/talking-cat.webp",
        "category_id": 1,
    },
    {
        "name": "Нейтрализатор памяти",
        "description": "Сотрите неудачный момент из памяти. Просто и эффективно!",
        "price_shmeckles": 3499,
        "price_flurbos": 2274,
        "price_credits": 2589,
        "image_url": "/images/memory-neutralizer.webp",
        "category_id": 3,
    },
    {
        "name": "Мега-семена",
        "description": "Придают временный но невероятный интеллект. Внимание: эффект недолговечен!",
        "price_shmeckles": 599,
        "price_flurbos": 389,
        "price_credits": 443,
        "image_url": "/images/mega-seeds.webp",
        "category_id": 2,
    },
    {
        "name": "Микро-вселенная",
        "description": "Источник энергии. Её жители поклоняются вам как богу!",
        "price_shmeckles": 25000,
        "price_flurbos": 16250,
        "price_credits": 18500,
        "image_url": "/images/microverse-battery.webp",
        "category_id": 3,
    },
]

CATEGORIES = [
    {"name": "Волшебные предметы", "description": "Товары с магическими свойствами"},
    {"name": "Помощники дома", "description": "Предметы для облегчения быта"},
    {"name": "Редкости", "description": "Уникальные и редкие вещи"},
]


async def seed_database():
    """Заполнить БД тестовыми данными"""
    print("🔧 Инициализирую БД...")
    print(f"📊 Base.metadata.tables: {list(Base.metadata.tables.keys())}")
    
    engine = create_async_engine(DATABASE_URL, echo=False)

    # 1️⃣ СНАЧАЛА СОЗДАЕМ ТАБЛИЦЫ
    async with engine.begin() as conn:
        print("📝 Создаю таблицы...")
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы созданы")

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # Проверяем, есть ли уже данные
        result = await session.execute(select(Category))
        existing_categories = result.scalars().all()

        if not existing_categories:
            print("📝 Создаю категории...")
            for cat_data in CATEGORIES:
                category = Category(**cat_data)
                session.add(category)
            await session.commit()
            print("✅ Категории созданы")
        else:
            print(f"ℹ️ Категории уже есть ({len(existing_categories)} штук)")

        # Проверяем товары
        result = await session.execute(select(Product))
        existing_products = result.scalars().all()

        if not existing_products:
            print("📝 Создаю товары...")
            for prod_data in PRODUCTS:
                product = Product(**prod_data)
                session.add(product)
            await session.commit()
            print(f"✅ Товары созданы ({len(PRODUCTS)} штук)")
        else:
            print(f"ℹ️ Товары уже существуют ({len(existing_products)} штук)")

    await engine.dispose()
    print("✅ БД готова к использованию!")


if __name__ == "__main__":
    asyncio.run(seed_database())