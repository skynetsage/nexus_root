from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends , HTTPException, UploadFile

from ..schemas.file import FileCreate, FileResponse
from ..schemas.resume import ResumeCreate, ResumeResponse
from ..db.postgres.repositories.file_repository import FileRepository
from ..db.postgres.repositories.resume_repository import ResumeRepository
from ..config.logger import get_logger
from ..utils.file_util import upload_file
from ..utils.resume_util import gen_custom_resume_id

logger = get_logger("resume")

class ResumeController:
    def __init__(self, db: AsyncSession):
        self.file_repo = FileRepository(db)
        self.resume_repo = ResumeRepository(db)

    async def upload_resume(self, file: UploadFile) -> FileResponse:
        try:
            file_path = await upload_file(file)
            logger.info(f"File uploaded successfully: {file_path}")
            custom_id = gen_custom_resume_id("dash")

            resume_entry = ResumeCreate(
                resume_id=custom_id,
                analysis_id=None,
                is_analyzed=False,
                is_active=True
            )
            await self.resume_repo.create_resume(resume_entry)
            logger.info("Resume entry created successfully")

            file_entry = FileCreate(
                filename=file.filename,
                filepath=file_path,
                resume_id=custom_id,
                is_active=True
            )
            res = await self.file_repo.create_file(file_entry)
            logger.info("File entry created successfully")

            return FileResponse(
                id=res.id,
                filename=res.filename,
                filepath=res.filepath,
                resume_id=res.resume_id,
                is_active=res.is_active,
                created_at=res.created_at,
                updated_at=res.updated_at
            )
        except ValueError as ve:
            logger.error(f"Invalid file type: {ve}")
            raise HTTPException(status_code=400, detail=str(ve))
        except FileNotFoundError as e:
            logger.error(f"File upload failed: {e}")
            raise HTTPException(status_code=500, detail="File upload failed")
        except Exception as e:
            logger.error(f"An error occurred while uploading the file: {e}")
            raise HTTPException(status_code=500, detail="An error occurred while processing the file")





