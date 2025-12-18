from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Класс для управления настройками приложения.
    
    Загружает значения из:
    1. Переменных окружения
    2. Файла .env
    
    Использование:
        from config import settings
        print(settings.tg_bot_key)
    """
    
    tg_bot_key: str = Field(
        ...,
        description="Telegram Bot API Key",
        alias="TG_BOT_KEY"
    )
    
    class Config:
        """Конфигурация для Settings"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Создаём глобальный экземпляр настроек
settings = Settings()
