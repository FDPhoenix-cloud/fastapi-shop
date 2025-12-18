from data.products import products

def get_next_id() -> int:
    """
    Генерирует следующий доступный ID для нового продукта.
    
    Находит максимальный ID в списке продуктов и возвращает значение на 1 больше.
    Если список пуст, возвращает 1.
    
    Returns:
        int: Следующий доступный ID
    """
    if not products:
        return 1
    
    max_id = max(product["id"] for product in products)
    return max_id + 1
