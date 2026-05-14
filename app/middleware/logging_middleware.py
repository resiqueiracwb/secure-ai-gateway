import time

from starlette.middleware.base import (
    BaseHTTPMiddleware
)

from app.utils.logger import logger


class LoggingMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next
    ):

        start_time = time.time()

        logger.info(
            f"Request started: "
            f"{request.method} {request.url.path}"
        )

        response = await call_next(request)

        duration = time.time() - start_time

        logger.info(
            f"Request completed in "
            f"{duration:.4f}s"
        )

        return response