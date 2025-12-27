import logging
import uuid
from pathlib import Path

from fastapi import UploadFile, HTTPException

logger = logging.getLogger(__name__)

# uploads/products относительно корня проекта
UPLOAD_DIR = Path("uploads") / "products"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 МБ


async def save_product_image(file: UploadFile) -> str:
    """
    Сохраняет файл изображения товара на диск, возвращает URL (/uploads/products/xxx.ext).
    """
    logger.info(f"📥 Начало загрузки файла: {file.filename}")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        logger.error(f"❌ Недопустимый формат файла: {ext}")
        raise HTTPException(
            status_code=400,
            detail=f"Разрешены только: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        logger.error(f"❌ Файл слишком большой: {len(content)} байт")
        raise HTTPException(
            status_code=400,
            detail="Максимальный размер файла — 5 МБ",
        )

    filename = f"{uuid.uuid4()}{ext}"
    filepath = UPLOAD_DIR / filename

    try:
        with filepath.open("wb") as f:
            f.write(content)
    except Exception as e:
        logger.exception(f"🔥 Ошибка сохранения файла {filepath}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось сохранить файл",
        )

    logger.info(f"✅ Файл сохранён: {filepath}")
    return f"/uploads/products/{filename}"


def delete_product_image(image_url: str) -> bool:
    """
    Удаляет файл изображения по URL (/uploads/products/xxx.ext).
    Возвращает True, если файл удалён, False — если его не было или произошла ошибка.
    """
    try:
        filename = Path(image_url).name
        filepath = UPLOAD_DIR / filename

        if filepath.exists():
            filepath.unlink()
            logger.info(f"🗑️ Файл удалён: {filepath}")
            return True
        else:
            logger.warning(f"⚠️ Файл для удаления не найден: {filepath}")
            return False
    except Exception as e:
        logger.exception(f"🔥 Ошибка при удалении файла {image_url}: {e}")
        return False
