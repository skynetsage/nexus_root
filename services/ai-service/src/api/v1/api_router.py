from fastapi import APIRouter
from .endpoints.analyzer import resume_analyzer_router
from ...config.settings import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(resume_analyzer_router, tags=["resumes"])