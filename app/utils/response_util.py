from fastapi import status
from fastapi.responses import JSONResponse
from typing import Any, Optional


def success_response(
    data: Any = None,
    message: str = "Success",
    code: int = status.HTTP_200_OK,
) -> JSONResponse:
    if not str(code).startswith("2"):
        raise ValueError(f"Status code {code} is not a success code (2xx)")
    return JSONResponse(
        status_code=code,
        content={
            "status": "success",
            "message": message,
            "data": data,
        },
    )


def error_response(
    message: str = "Bad Request",
    code: int = status.HTTP_400_BAD_REQUEST,
    errors: Optional[Any] = None,
) -> JSONResponse:
    if not str(code).startswith("4"):
        raise ValueError(f"Status code {code} is not an error code (4xx)")
    content = {
        "status": "error",
        "message": message,
    }
    if errors:
        content["errors"] = errors
    return JSONResponse(status_code=code, content=content)


def server_error_response(
    message: str = "Server Error",
    code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    errors: Optional[Any] = None,
) -> JSONResponse:
    if not str(code).startswith("5"):
        raise ValueError(f"Status code {code} is not a server error code (5xx)")
    content = {
        "status": "error",
        "message": message,
    }
    if errors:
        content["errors"] = errors
    return JSONResponse(
        status_code=code,
        content=content,
    )
