from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware

class HealthCheckMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if request.url.path.startswith("/api/v1/health"):
            postgres_ok = getattr(request.app.state, "postgres_healthy", True)
            mongo_ok = getattr(request.app.state, "mongo_healthy", True)

            if not (postgres_ok and mongo_ok):
                response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return response