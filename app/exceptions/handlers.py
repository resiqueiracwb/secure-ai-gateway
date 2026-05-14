from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.logger import logger

from app.exceptions.custom_exceptions import (
    ProviderNotSupportedException
)


async def provider_not_supported_handler(
    request: Request,
    exc: ProviderNotSupportedException
):
    logger.error(
        f"Unsupported provider received: "
        f"{exc.provider}"
    )

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "code": "INVALID_PROVIDER",
                "message": (
                    f"Provider '{exc.provider}' "
                    f"is not supported"
                )
            }
        }
    )