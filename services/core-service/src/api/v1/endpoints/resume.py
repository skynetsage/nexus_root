from fastapi import APIRouter, UploadFile, Depends, status, File
from sqlalchemy.ext.asyncio import AsyncSession

from ....controllers.resume_controller import ResumeController
from ....db.postgres.engine import get_db

resume_router = APIRouter(prefix="/resumes")

@resume_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),   
    db: AsyncSession = Depends(get_db)
):
    controller = ResumeController(db=db)
    return await controller.upload_resume(file=file)


