from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_async_session
from models.user import User

async def get_mock_user(
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """Получить первого пользователя (для тестирования)"""
    stmt = select(User).limit(1)
    result = await session.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователей не найдено. Создайте пользователя!"
        )
    return user
