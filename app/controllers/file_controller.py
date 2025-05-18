import uuid
from fastapi import UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres.repository import (
    ResumeRepository,
    FileUploadRepository,
    UserRepository,
)
from app.services.file_service import FileService

from app.core.logger import get_logger

logger = get_logger("file")


class FileController:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.file_service = FileService(
            user_repo=UserRepository(db),
            resume_repo=ResumeRepository(db),
            upload_repo=FileUploadRepository(db),
        )

    async def handle_upload(self, user_id: int, file: UploadFile):
        if not file or not file.filename:
            logger.error("No file provided for upload")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided"
            )

        try:
            result = await self.file_service.upload_resume(user_id, file)
        except Exception as e:
            logger.error(f"Exception during file upload: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred while uploading resume",
            )

        if not result:
            logger.error("Failed to upload resume")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Error uploading resume"
            )

        logger.info(f"Resume uploaded successfully: {result}")
        return result

    # async def handle_get_resume(self, user_id: int):
    #     if not user_id:
    #         logger.error("No user ID provided")
    #         return JSONResponse(
    #             status_code=400, content={"message": "No user ID provided"}
    #         )
    #     result = await self.file_service.get_resume_by_userid(user_id)
    #     if not result:
    #         logger.error("Error getting resume")
    #         return JSONResponse(
    #             status_code=400, content={"message": "Error getting resume"}
    #         )
    #     logger.info("Resume retrieved successfully", obj=result)
    #     return JSONResponse(status_code=200, content=result)
