from fastapi import FastAPI

from app.routes.ai import router as ai_router
from app.config.settings import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Modern AI-ready backend API"
)
app.include_router(ai_router)