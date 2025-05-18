import traceback

from fastapi import (
    APIRouter,
    Form,
    UploadFile,
    File,
    Depends,
    status,
    Body,
    HTTPException,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.file_controller import FileController
from app.db.postgres.engine import get_db


file_router = APIRouter(prefix="/file", tags=["file"])


@file_router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        controller = FileController(db)
        return await controller.handle_upload(user_id, file)
    except Exception as e:
        print("=== FULL TRACEBACK ===")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail="Unexpected error occurred while uploading resume"
        )


@file_router.get("/getAllResume/{user_id}")
async def get_all_resume(user_id: int, db: AsyncSession = Depends(get_db)):
    controller = FileController(db)
    return await controller.handle_get_resume(user_id)
