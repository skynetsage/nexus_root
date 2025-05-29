from fastapi import APIRouter, UploadFile, Depends, status, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from ....controllers.resume_controller import ResumeController
from ....db.postgres.engine import get_db

resume_router = APIRouter(prefix="/resumes")

@resume_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resume(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    controller = ResumeController(db=db)
    return await controller.upload_resume(user_id=user_id,file=file)


@resume_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_resumes(
    user_id: int,
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    controller = ResumeController(db=db)
    return await controller.get_all_resumes_for_user(user_id=user_id, limit=limit, offset=offset)



