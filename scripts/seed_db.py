import asyncio

from core.database import AsyncSessionLocal, init_db
from models.product import Product


async def seed_database() -> None:
    """
    Заполнение базы данных тестовыми продуктами.
    ВАЖНО: init_db() дропает и создаёт таблицы заново.
    """
    await init_db()

    products_data = [
        {
            "name": "Стандартный Плюмбус",
            "description": "Каждый дом должен иметь плюмбус. Мы не знаем, что он делает, но он делает это очень хорошо. В комплекте: шлее, грумбо и флиб.",
            "image_url": "/images/plumbus.webp",
            "price_shmeckles": 6.5,
            "price_credits": 4.8,
            "price_flurbos": 3.2,
        },
        {
            "name": "Коробка с Мисиксами",
            "description": "Нужна помощь по дому? Нажмите кнопку, и появится Мисикс, готовый выполнить одно ваше поручение. Существование для него — боль, так что не затягивайте!",
            "image_url": "/images/meeseeks-box.webp",
            "price_shmeckles": 19.99,
            "price_credits": 14.5,
            "price_flurbos": 9.8,
        },
        {
            "name": "Портальная пушка (б/у)",
            "description": "Слегка поцарапана, заряд портальной жидкости на 37%. Возврату не подлежит. Может пахнуть приключениями и чужими измерениями. Осторожно: привлекает внимание Цитадели.",
            "image_url": "/images/portal-gun.webp",
            "price_shmeckles": 9999.99,
            "price_credits": 7500.0,
            "price_flurbos": 4999.99,
        },
        {
            "name": "Концентрированная темная материя",
            "description": "Идеальное топливо для вашего космического корабля. Всего одна капля позволит вам улететь от любых экзистенциальных кризисов. Не употреблять внутрь!",
            "image_url": "/images/dark-matter.webp",
            "price_shmeckles": 850.0,
            "price_credits": 620.0,
            "price_flurbos": 415.0,
        },
        {
            "name": "Масло-робот 'Передай масло'",
            "description": "Его единственная цель существования — передавать масло. Он осознает это и впадает в депрессию. Отличный собеседник для завтрака в одиночестве.",
            "image_url": "/images/butter-robot.webp",
            "price_shmeckles": 25.5,
            "price_credits": 18.2,
            "price_flurbos": 12.5,
        },
        {
            "name": "Шлем для чтения мыслей собак",
            "description": "Теперь вы наконец-то узнаете, где ваш пёс спрятал тапки и почему он лает на пылесос. Спойлер: он считает вас хорошим мальчиком.",
            "image_url": "/images/dog-helmet.webp",
            "price_shmeckles": 120.0,
            "price_credits": 88.0,
            "price_flurbos": 59.0,
        },
        {
            "name": "Зерновые 'Глазастики'",
            "description": "Маленькие глазастые человечки, которые живут в коробке и умоляют вас съесть их. Сбалансированный завтрак с нотками отчаяния.",
            "image_url": "/images/eyeholes.webp",
            "price_shmeckles": 4.20,
            "price_credits": 3.1,
            "price_flurbos": 2.05,
        },
        {
            "name": "Микро-вселенная в коробке",
            "description": "Источник энергии для вашего автомобиля. Её жители поклоняются вам как богу, пока вы не заводите машину. Этично? Решать вам.",
            "image_url": "/images/microverse-battery.webp",
            "price_shmeckles": 2500.0,
            "price_credits": 1850.0,
            "price_flurbos": 1225.0,
        },
        {
            "name": "Нейтрализатор памяти",
            "description": "Видели что-то, что не следовало? Сотрите этот момент из своей памяти или памяти друзей. Побочный эффект: возможно, вы забудете, как завязывать шнурки.",
            "image_url": "/images/memory-neutralizer.webp",
            "price_shmeckles": 350.75,
            "price_credits": 256.0,
            "price_flurbos": 172.5,
        },
        {
            "name": "Семена из Мега-деревьев",
            "description": "Придают временный, но невероятный интеллект. Для провоза необходимо поместить в очень... укромное место. Таможня не одобрит.",
            "image_url": "/images/mega-seeds.webp",
            "price_shmeckles": 55.0,
            "price_credits": 40.5,
            "price_flurbos": 27.0,
        },
        {
            "name": "Анатомический парк (Набор 'Сделай сам')",
            "description": "Уменьшитесь и постройте парк развлечений внутри бездомного! В наборе все аттракционы: 'Пиратская Селезенка', 'Костяной Экспресс' и другие. Бездомный в комплект не входит.",
            "image_url": "/images/anatomy-park.webp",
            "price_shmeckles": 199.99,
            "price_credits": 146.0,
            "price_flurbos": 98.5,
        },
        {
            "name": "Кристалл смерти",
            "description": "Показывает все возможные варианты вашей смерти в зависимости от ваших действий. Идеально для прокрастинаторов и ипохондриков.",
            "image_url": "/images/death-crystal.webp",
            "price_shmeckles": 77.0,
            "price_credits": 56.5,
            "price_flurbos": 37.8,
        },
        {
            "name": "Говорящий кот (без гарантий)",
            "description": "Он умеет говорить, но лучше бы вы не знали, о чём. Не спрашивайте его, что он видел. Просто кормите и надейтесь на лучшее.",
            "image_url": "/images/talking-cat.webp",
            "price_shmeckles": 5.0,
            "price_credits": 3.6,
            "price_flurbos": 2.4,
        },
        {
            "name": "Ботинки для ходьбы по стенам",
            "description": "Гравитация — для слабаков. Теперь пол, стены и потолок — это просто разные направления для прогулки. Не рекомендуется использовать после плотного обеда.",
            "image_url": "/images/gravity-shoes.webp",
            "price_shmeckles": 210.0,
            "price_credits": 154.0,
            "price_flurbos": 103.0,
        },
        {
            "name": "Прибор для управления снами",
            "description": "Проникните в сны вашего учителя математики и заставьте его поставить вам пятерку. Или просто покатайтесь на динозавре. Возможности безграничны!",
            "image_url": "/images/dream-inator.webp",
            "price_shmeckles": 400.0,
            "price_credits": 292.0,
            "price_flurbos": 196.0,
        },
        {
            "name": "Клон-пистолет",
            "description": "Создает нестабильную копию любого живого существа. Копия может растаять через час. Идеально, чтобы отправить клона на скучное совещание.",
            "image_url": "/images/clone-gun.webp",
            "price_shmeckles": 555.55,
            "price_credits": 405.0,
            "price_flurbos": 272.5,
        },
        {
            "name": "Пистолет-уменьшитель",
            "description": "Уменьшает любой предмет или существо до карманного размера. Полезно для переездов или если вы просто хотите гигантский бутерброд, который поместится в руке.",
            "image_url": "/images/shrinking-ray.webp",
            "price_shmeckles": 320.0,
            "price_credits": 234.0,
            "price_flurbos": 157.0,
        },
        {
            "name": "Крем 'Вечная молодость'",
            "description": "Останавливает процесс старения. Необратимо. Подумайте дважды, прежде чем использовать его на своем ребенке. Инструкция прилагается, но кто ее читает?",
            "image_url": "/images/age-cream.webp",
            "price_shmeckles": 680.0,
            "price_credits": 496.0,
            "price_flurbos": 334.0,
        },
        {
            "name": "Симулятор 'Рой'",
            "description": "Проживите целую жизнь обычного парня по имени Рой. Осторожно, вызывает привыкание и заставляет задуматься о ценности ковров.",
            "image_url": "/images/roy-game.webp",
            "price_shmeckles": 12.50,
            "price_credits": 9.15,
            "price_flurbos": 6.1,
        },
        {
            "name": "Гармонизатор межвселенского ТВ",
            "description": "Подключается к вашему обычному телевизору и открывает доступ к бесконечному числу каналов со всей мультивселенной. Включая рекламу 'Глазастиков' и сериал 'Мистикс-полицейский'.",
            "image_url": "/images/interdimensional-cable.webp",
            "price_shmeckles": 49.99,
            "price_credits": 36.5,
            "price_flurbos": 24.5,
        },
    ]

    async with AsyncSessionLocal() as session:
        for data in products_data:
            session.add(Product(**data))
        await session.commit()

    print(f"Добавлено {len(products_data)} продуктов в базу данных.")


if __name__ == "__main__":
    asyncio.run(seed_database())
