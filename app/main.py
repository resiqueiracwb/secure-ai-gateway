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


app = FastAPI(
    title=settings.APP_NAME or "Secure AI Gateway",
    version=settings.APP_VERSION or "1.0.0",
    description="Modern AI-ready backend API"
)
app.include_router(ai_router)

app.add_exception_handler(
    ProviderNotSupportedException,
    provider_not_supported_handler
)

app.add_middleware(
    LoggingMiddleware
)

app.include_router(auth_router)