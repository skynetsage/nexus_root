import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.logger import get_logger  # Adjust if path differs

logger = get_logger("http")


class HTTPLoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response: Response = None

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            logger.info(
                f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s",
                {
                    "client": request.client.host,
                    "query_params": dict(request.query_params),
                    "headers": dict(request.headers),
                }
            )
            return response
        except Exception as exc:
            process_time = time.time() - start_time
            logger.error(
                f"Unhandled exception for {request.method} {request.url.path} - {process_time:.2f}s",
                obj={"client": request.client.host},
                exc_info=True
            )
            raise
