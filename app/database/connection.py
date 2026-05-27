import os

from sqlalchemy import create_engine
from app.core.settings import (
    settings
)

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL
)
