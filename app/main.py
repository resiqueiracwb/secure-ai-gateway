from fastapi import FastAPI

from app.routes.ai import router as ai_router
from app.config.settings import settings
from app.exceptions.handlers import (
    provider_not_supported_handler
)

from app.exceptions.custom_exceptions import (
    ProviderNotSupportedException
)

from app.middleware.logging_middleware import (
    LoggingMiddleware
)

from app.routes.auth import (
    router as auth_router
)

from app.database.connection import (
    engine
)

from app.database.base import Base

from app.entities.user_entity import (
    UserEntity
)

from app.middleware.request_context_middleware import (
    RequestContextMiddleware
)

from app.routes.health import (
    router as health_router
)
from app.core.settings import (
    settings
)
from app.routes.async_demo import (
    router as async_demo_router
)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Modern AI-ready backend API"
)
app.add_middleware(
    RequestContextMiddleware
)

app.include_router(ai_router)

app.add_exception_handler(
    ProviderNotSupportedException,
    provider_not_supported_handler
)

app.add_middleware(
    LoggingMiddleware
)

app.include_router(
    health_router
)
app.include_router(
    async_demo_router
)
app.include_router(auth_router)