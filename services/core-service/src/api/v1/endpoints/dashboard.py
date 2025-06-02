from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....controllers.dashboard_controller import DashboardController
from ....db.postgres.engine import get_db

dashboard_router = APIRouter(prefix="/dashboard")


@dashboard_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_dashboard_data(user_id: int, db: AsyncSession = Depends(get_db)):
    controller = DashboardController(db=db)
    return await controller.gen_dashboard_data(user_id=user_id)
