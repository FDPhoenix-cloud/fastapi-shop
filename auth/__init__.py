from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from auth.backend import auth_backend
from auth.manager import get_user_manager
from models.user import User
from schemas.user import UserRead, UserCreate, UserUpdate

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)

auth_router = APIRouter()

# роуты аутентификации (логин, refresh, etc.)
auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

# роуты регистрации
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# роуты управления пользователем
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
