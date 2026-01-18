from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from auth.backend import auth_backend
from auth.manager import get_user_manager
from models.user import User
from schemas.user import UserRead, UserCreate, UserUpdate

# Инициализация FastAPIUsers
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Текущий активный пользователь
current_active_user = fastapi_users.current_user(active=True)

# Создаем роутер для всех auth эндпойнтов
auth_router = APIRouter()

# 1. Роутер аутентификации (логин, logout, refresh)
auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/auth",
    tags=["auth"],
)

# 2. Роутер регистрации
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)

# 3. Роутер управления пользователем (GET /api/auth/me, PATCH /api/auth/... etc)
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/auth",
    tags=["auth"],
)

__all__ = ["auth_router", "current_active_user", "fastapi_users"]