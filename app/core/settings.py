from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(
    BaseSettings
):
    model_config = SettingsConfigDict(
        env_file=".env"
    )

    APP_NAME: str
    APP_VERSION: str

    DATABASE_URL: str

    JWT_SECRET: str

    DEBUG: bool = False

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


settings = Settings()
