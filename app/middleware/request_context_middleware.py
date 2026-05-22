import time
import uuid

from starlette.middleware.base import (
    BaseHTTPMiddleware
)

from fastapi import Request

from app.utils.logger import logger


class RequestContextMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        request_id = str(
            uuid.uuid4()
        )

        start_time = time.time()

        request.state.request_id = (
            request_id
        )

        logger.info(
            "Request started",
            extra={
                "event": "request_started",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path
            }
        )

        response = await call_next(
            request
        )

        process_time = round(
            (
                time.time() - start_time
            ) * 1000,
            2
        )

        logger.info(
            "Request completed",
            extra={
                "event": "request_completed",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "latency_ms": process_time
            }
        )

        response.headers[
            "X-Request-ID"
        ] = request_id

        return response