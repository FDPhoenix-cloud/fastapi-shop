from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    full_name: Optional[str] = None


class UserCreate(schemas.BaseUserCreate):
    full_name: Optional[str] = None

    # запрещаем передавать флаги is_active, is_superuser, is_verified
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserUpdate(schemas.BaseUserUpdate):
    full_name: Optional[str] = None
