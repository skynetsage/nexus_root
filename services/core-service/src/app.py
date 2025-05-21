from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .config.settings import settings
from .db.postgres.engine import get_db

app = FastAPI(
    title="Core Service",
    description="Core service for the Nexus",
    version="1.0.0",
)

api_router = APIRouter()

@api_router.get("/")
async def root():
    return {"message": "Welcome to the Core Service!"}

@api_router.get("/health/db")
async def db_check(session: AsyncSession = Depends(get_db)):
    return { "status": "ok" }

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,  # Enable reload for development
    )