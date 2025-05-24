from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ....db.postgres.engine import get_db

health_router = APIRouter(prefix="/health")

@health_router.get("/db", status_code=status.HTTP_200_OK)
async def db_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}"
        )