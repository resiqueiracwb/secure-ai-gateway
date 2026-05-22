from fastapi import (
    APIRouter,
    status
)

from sqlalchemy import text

from app.database.session import (
    SessionLocal
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
def health_check():

    return {
        "status": "healthy"
    }