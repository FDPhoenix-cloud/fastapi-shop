"""
Модуль конвертации валют для магазина Рика и Морти
"""

from enum import Enum


class Currency(str, Enum):
    """Поддерживаемые валюты"""
    SHMECKLES = "shmeckles"
    FLURBOS = "flurbos"
    CREDITS = "credits"


# Символы валют для отображения
CURRENCY_SYMBOLS = {
    Currency.SHMECKLES: "₴",    # Шмекели
    Currency.FLURBOS: "₣",      # Флурбо
    Currency.CREDITS: "₲",      # Кредиты
}

# Описания валют
CURRENCY_NAMES = {
    Currency.SHMECKLES: "Шмекели",
    Currency.FLURBOS: "Флурбо",
    Currency.CREDITS: "Кредиты",
}

# Курсы конвертации (по отношению к Шмекелям)
# 1 Шмекель = X других валют
CONVERSION_RATES = {
    Currency.SHMECKLES: 1.0,
    Currency.FLURBOS: 0.65,      # 1 Шмекель = 0.65 Флурбо
    Currency.CREDITS: 0.74,      # 1 Шмекель = 0.74 Кредита
}


def convert_price(price_shmeckles: float, target_currency: Currency) -> float:
    """
    Конвертирует цену из шмекелей в целевую валюту.
    
    Args:
        price_shmeckles: Цена в шмекелях
        target_currency: Целевая валюта
        
    Returns:
        Конвертированная цена, округленная до 2 знаков
    """
    if target_currency not in CONVERSION_RATES:
        raise ValueError(f"Неизвестная валюта: {target_currency}")
    
    return round(price_shmeckles * CONVERSION_RATES[target_currency], 2)


def format_price(price: float, currency: Currency) -> str:
    """
    Форматирует цену с символом валюты.
    
    Args:
        price: Числовое значение цены
        currency: Валюта
        
    Returns:
        Отформатированная строка вида "₴1,299.99"
    """
    symbol = CURRENCY_SYMBOLS[currency]
    return f"{symbol}{price:,.2f}"


def get_currency_display_name(currency: Currency) -> str:
    """Получить читаемое имя валюты"""
    return CURRENCY_NAMES.get(currency, str(currency))
