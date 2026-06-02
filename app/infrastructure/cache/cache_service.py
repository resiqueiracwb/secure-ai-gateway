from app.infrastructure.cache.redis_client import (
    redis_client
)


async def get_cache(
    key: str
):

    return await redis_client.get(
        key
    )


async def set_cache(
    key: str,
    value: str,
    ttl: int = 300
):

    await redis_client.set(
        key,
        value,
        ex=ttl
    )


async def delete_cache(
    key: str
):

    await redis_client.delete(
        key
    )
