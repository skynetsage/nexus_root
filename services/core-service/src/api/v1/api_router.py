from fastapi import APIRouter
from .endpoints.health_check import health_router
from .endpoints.resume import resume_router
from ...config.settings import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(health_router, tags=["health"])
api_router.include_router(resume_router, tags=["resumes"])
