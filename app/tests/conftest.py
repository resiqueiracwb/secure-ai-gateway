import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://admin:admin@localhost:5432/secure_ai_gateway"
)

os.environ.setdefault(
    "REDIS_HOST",
    "localhost"
)
