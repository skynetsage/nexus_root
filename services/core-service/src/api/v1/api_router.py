from fastapi import APIRouter
from .endpoints.health_check import health_router
from .endpoints.resume import resume_router
from .endpoints.user import user_router
from .endpoints.dashboard import dashboard_router
from ...config.settings import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(health_router, tags=["health"])
api_router.include_router(resume_router, tags=["resumes"])
api_router.include_router(user_router, tags=["users"])
api_router.include_router(dashboard_router, tags=["dashboard"])
