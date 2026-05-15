from typing import Any, Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    message: str


class BaseResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[ErrorResponse] = None