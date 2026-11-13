from typing import Any

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    status_code: int
    message: str
    errors: list[ErrorDetail] | None = None
    path: str