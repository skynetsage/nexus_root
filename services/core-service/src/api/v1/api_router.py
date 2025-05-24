from fastapi import FastAPI, APIRouter
from .endpoints.health_check import health_router
from ...config.settings import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(health_router, tags=["health"])
