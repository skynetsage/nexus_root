from fastapi import FastAPI, APIRouter
from src.config.settings import settings
from src.db.postgres.engine import get_db
from sqlalchemy import text

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
async def health_db():
    async with get_db() as session:
        try:

            await session.execute(text("SELECT 1"))
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
        
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,  # Enable reload for development
    )