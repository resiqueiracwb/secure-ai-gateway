import json
import logging
import sys


class JsonFormatter(
    logging.Formatter
):

    def format(
        self,
        record
    ):

        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        }

        if hasattr(
            record,
            "event"
        ):
            log_record["event"] = (
                record.event
            )

        if hasattr(
            record,
            "request_id"
        ):
            log_record["request_id"] = (
                record.request_id
            )

        if hasattr(
            record,
            "method"
        ):
            log_record["method"] = (
                record.method
            )

        if hasattr(
            record,
            "path"
        ):
            log_record["path"] = (
                record.path
            )

        if hasattr(
            record,
            "status_code"
        ):
            log_record[
                "status_code"
            ] = record.status_code

        if hasattr(
            record,
            "latency_ms"
        ):
            log_record[
                "latency_ms"
            ] = record.latency_ms

        return json.dumps(
            log_record
        )


logger = logging.getLogger(
    "secure-ai-gateway"
)

logger.setLevel(
    logging.INFO
)

handler = logging.StreamHandler(
    sys.stdout
)

handler.setFormatter(
    JsonFormatter()
)

logger.handlers.clear()

logger.addHandler(
    handler
)