from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
Класс для управления настройками приложения.
Загружает значения из .env и переменных окружения.
"""
    
    tg_bot_key: str = Field(
        ...,
        description="Telegram Bot API Key",
        alias="TG_BOT_KEY"
    )
    
    telegram_bot_api_key: str = Field(
    ...,
    description="Telegram Bot API token",
    alias="TELEGRAM_BOT_API_KEY",
)

    telegram_user_id: str = Field(
    ...,
    description="Telegram chat ID получателя уведомлений",
    alias="TELEGRAM_USER_ID",
)
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
