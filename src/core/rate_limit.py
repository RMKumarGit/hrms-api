
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse


def rate_limit_exceeded_response(
    request: Request,
    result: Any
) -> JSONResponse:

    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "status_code": 429,
            "message": "Too many requests. Please try again later.",
            "errors": None,
            "path": request.url.path
        },
        headers={
            "Retry-After": str(result.retry_after)
        }
    )
