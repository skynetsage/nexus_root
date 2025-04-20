from fastapi import APIRouter
from app.api.v1.endpoints.auth import auth_router
from app.api.v1.endpoints.health import db_router
from app.api.v1.endpoints.file import file_router
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(auth_router)
api_router.include_router(db_router)
api_router.include_router(file_router)
