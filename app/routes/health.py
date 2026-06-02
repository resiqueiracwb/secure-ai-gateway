from fastapi import (
    APIRouter,
    status
)

from sqlalchemy import text

from app.database.session import (
    SessionLocal
)

from app.infrastructure.cache.cache_service import (
    ping_cache
)

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get(
    "/live",
    status_code=status.HTTP_200_OK
)
def liveness_check():

    return {
        "status": "alive"
    }


@router.get(
    "/ready",
    status_code=status.HTTP_200_OK
)
def readiness_check():

    db = SessionLocal()

    try:

        db.execute(
            text("SELECT 1")
        )

        return {
            "status": "ready",
            "database": "connected"
        }

    except Exception:

        return {
            "status": "not_ready",
            "database": "disconnected"
        }

    finally:

        db.close()


@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def health_check():

    redis_connected = await ping_cache()

    db = SessionLocal()

    try:

        db.execute(
            text("SELECT 1")
        )

        database_connected = True

    except Exception:

        database_connected = False

    finally:

        db.close()

    overall_status = (
        "healthy"
        if (
            redis_connected
            and database_connected
        )
        else "degraded"
    )

    return {
        "status": overall_status,
        "database": (
            "up"
            if database_connected
            else "down"
        ),
        "redis": (
            "up"
            if redis_connected
            else "down"
        )
    }