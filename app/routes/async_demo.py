import asyncio

from fastapi import (
    APIRouter
)

router = APIRouter(
    prefix="/async",
    tags=["Async Demo"]
)


@router.get(
    "/demo"
)
async def async_demo():

    await asyncio.sleep(2)

    return {
        "message": "Async request completed"
    }   