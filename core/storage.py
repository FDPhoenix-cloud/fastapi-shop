import os
import uuid
import logging
from pathlib import Path
from fastapi import UploadFile, HTTPException

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads/products")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

async def save_product_image(file: UploadFile) -> str:
    """
    Сохраняет изображение товара и возвращает путь.
    """
    
    # Проверка имени файла
    if not file.filename:
        raise HTTPException(status_code=400, detail="Имя файла отсутствует")
    
    # Проверка расширения
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Расширение .{ext} не поддерживается. Допустимые: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Читаем содержимое
    content = await file.read()
    
    # Проверка размера
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"Файл слишком большой (макс {MAX_FILE_SIZE // 1024 // 1024}MB)"
        )
    
    # Генерируем уникальное имя
    unique_id = uuid.uuid4().hex
    new_filename = f"{unique_id}.{ext}"
    file_path = UPLOAD_DIR / new_filename
    
    # Сохраняем файл
    try:
        with open(file_path, "wb") as f:
            f.write(content)
        logger.info(f"✅ Изображение сохранено: {new_filename}")
    except Exception as e:
        logger.exception(f"❌ Ошибка при сохранении файла: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось сохранить изображение"
        )
    
    return f"/uploads/products/{new_filename}"

def delete_product_image(image_url: str) -> bool:
    """
    Удаляет изображение товара с диска.
    Возвращает True если файл был удалён.
    """
    if not image_url:
        return False
    
    # Извлекаем имя файла из URL
    filename = image_url.split("/")[-1]
    file_path = UPLOAD_DIR / filename
    
    try:
        if file_path.exists():
            file_path.unlink()
            logger.info(f"✅ Изображение удалено: {filename}")
            return True
    except Exception as e:
        logger.exception(f"❌ Ошибка при удалении файла: {e}")
    
    return False
