from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://admin:admin@postgres:5432/secure_ai_gateway"
)

engine = create_engine(
    DATABASE_URL
)