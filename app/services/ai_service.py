from app.exceptions.custom_exceptions import (
    ProviderNotSupportedException
)

from app.infrastructure.cache.cache_service import (
    get_cache,
    set_cache
)

from app.infrastructure.cache.cache_keys import (
    ai_prompt_key
)

from app.utils.logger import (
    logger
)


class AIService:

    SUPPORTED_PROVIDERS = [
        "openai",
        "claude",
        "gemini"
    ]

    @staticmethod
    async def process_prompt(
        prompt: str,
        provider: str
    ):

        if provider not in AIService.SUPPORTED_PROVIDERS:
            raise ProviderNotSupportedException(
                provider
            )

        cache_key = ai_prompt_key(
            prompt
        )

        cached_response = await get_cache(
            cache_key
        )

        if cached_response:

            logger.info(
                "CACHE HIT",
                extra={
                    "cache_key": cache_key,
                    "provider": provider
                }
            )

            return cached_response

        logger.info(
            "CACHE MISS",
            extra={
                "cache_key": cache_key,
                "provider": provider
            }
        )

        response = prompt.strip().upper()

        await set_cache(
            cache_key,
            response,
            ttl=300
        )

        logger.info(
            "CACHE SET",
            extra={
                "cache_key": cache_key,
                "provider": provider,
                "ttl": 300
            }
        )

        return response
