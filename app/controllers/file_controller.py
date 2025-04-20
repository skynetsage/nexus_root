import uuid
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres.repository import (
    ResumeRepository,
    ResumeUploadRepository,
    UserResumeRepository,
    UserRepository,
)
from app.services.file_service import FileService

from app.core.logger import get_logger

logger = get_logger("file")


class FileController:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.file_service = FileService(
            UserRepository(db),
            ResumeRepository(db),
            ResumeUploadRepository(db),
            UserResumeRepository(db),
        )

    async def handle_upload(self, user_id: int, file: UploadFile):
        if not file.filename:
            logger.error("No file provided")
            return JSONResponse(
                status_code=400, content={"message": "No file provided"}
            )
        result = await self.file_service.upload_resume(user_id, file)
        if not result:
            logger.error("Error uploading resume")
            return JSONResponse(
                status_code=400, content={"message": "Error uploading resume"}
            )

        logger.info("Resume uploaded successfully", obj=result)
        return JSONResponse(status_code=200, content=result)

    async def handle_get_resume(self, user_id: int):
        if not user_id:
            logger.error("No user ID provided")
            return JSONResponse(
                status_code=400, content={"message": "No user ID provided"}
            )
        result = await self.file_service.get_resume_by_userid(user_id)
        if not result:
            logger.error("Error getting resume")
            return JSONResponse(
                status_code=400, content={"message": "Error getting resume"}
            )
        logger.info("Resume retrieved successfully", obj=result)
        return JSONResponse(status_code=200, content=result)
