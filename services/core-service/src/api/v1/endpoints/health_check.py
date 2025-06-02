from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ....db.postgres.engine import get_db
from ....db.mongo.mongo import mongodb  # <- add this

health_router = APIRouter(prefix="/health")

@health_router.get("/db", status_code=status.HTTP_200_OK)
async def db_check(db: AsyncSession = Depends(get_db)):
    try:
        # PostgreSQL check
        await db.execute(text("SELECT 1"))

        # MongoDB check
        await mongodb.command("ping")  # sends {"ping": 1}
        
        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}"
        )
