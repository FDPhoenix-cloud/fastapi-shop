from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from core.config import settings

SECRET = settings.secret_key

# ✅ ИСПОЛЬЗУЕМ CookieTransport (токен в куках, НЕ в JSON)
cookie_transport = CookieTransport(
    cookie_name="fastapiusersauth",
    cookie_httponly=True,
    cookie_samesite="lax",  # ⚠️ ВАЖНО для локального тестирования
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,  # ✅ Токен в куках!
    get_strategy=get_jwt_strategy,
)