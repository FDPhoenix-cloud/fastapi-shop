import logging
import telegram

from config import settings

logging.basicConfig(level=logging.INFO)


async def send_telegram_message(message: str, parse_mode: str = "Markdown") -> None:
    """
    Отправка сообщения в Telegram через бота.
    """
    try:
        bot = telegram.Bot(token=settings.telegram_bot_api_key)

        await bot.send_message(
            chat_id=settings.telegram_user_id,
            text=message,
            parse_mode=parse_mode,
        )

        logging.info(
            'Сообщение "%s" отправлено в чат %s',
            message,
            settings.telegram_user_id,
        )
    except Exception as e:
        logging.error(
            "Ошибка отправки сообщения в чат %s: %s",
            settings.telegram_user_id,
            e,
        )
        # по желанию можно пробросить дальше:
        # raise
