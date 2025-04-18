from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from app.controllers.user_controller import register, login
from app.db.postgres.engine import get_db
from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register")
async def register_route(request: Request, db: AsyncSession = Depends(get_db)):
    if request.headers.get("content-type") != "application/json":
        return JSONResponse(status_code=400, content={"error": "Missing JSON in request"})
    return await register(request, db)

@auth_router.post("/login")
async def login_route(request: Request, db: AsyncSession = Depends(get_db)):
    if request.headers.get("content-type") != "application/json":
        return JSONResponse(status_code=400, content={"msg": "Missing JSON in request"})
    return await login(request, db)
