from typing import Dict, Any, List

from fastapi import UploadFile
from app.db.postgres.repository import (
    ResumeRepository,
    ResumeUploadRepository,
    UserResumeRepository,
    UserRepository,
)
from app.db.postgres.models import (
    ResumeModel,
    ResumeUploadModel,
    UserResumeModel,
)
from app.utils.file_util import save_file, generate_custom_resume_id
from app.core.logger import get_logger

logger = get_logger("file")


class FileService:
    def __init__(
        self,
        user_repo=UserRepository,
        resume_repo=ResumeRepository,
        upload_repo=ResumeUploadRepository,
        userResume_repo=UserResumeRepository,
    ):
        self.resume_repo = resume_repo
        self.upload_repo = upload_repo
        self.userResume_repo = userResume_repo
        self.user_repo = user_repo

    async def upload_resume(self, user_id: int, file: UploadFile):
        try:
            filename = file.filename

            user_data = await self.user_repo.get_user_by_id(user_id=user_id)

            if not user_data:
                logger.error(f"User with ID {user_id} not found.")
                return None

            try:
                file_path = await save_file(file, filename)
                logger.info(f"File {filename} saved successfully.")
            except Exception as e:
                logger.error(f"Error saving file {filename}", e, exc_info=True)
                raise e
            custom_resume_id = generate_custom_resume_id(user_data.username)

            new_resume_entry = ResumeModel(
                resume_id=custom_resume_id, is_analysed=False
            )
            await self.resume_repo.create(new_resume_entry)

            new_upload_entry = ResumeUploadModel(
                resume_id=custom_resume_id,
                filename=filename,
                file_path=file_path,
                is_active=True,
            )
            await self.upload_repo.create(new_upload_entry)

            new_user_resume_entry = UserResumeModel(
                user_id=user_id, resume_id=custom_resume_id
            )
            await self.userResume_repo.create(new_user_resume_entry)

            logger.info(
                f"Resume {custom_resume_id} uploaded successfully for user {user_id}."
            )

            return {
                "resume_id": custom_resume_id,
                "user_id": str(user_id),
                "filename": filename,
                "file_path": file_path,
            }
        except Exception as e:
            logger.error(f"Error uploading resume for user {user_id}", e, exc_info=True)
            raise e

    async def get_resume_by_userid(self, user_id: int) -> Dict[str, Any]:
        try:
            user = await self.user_repo.get_user_by_id(user_id=user_id)
            if not user:
                logger.debug(f"User with ID {user_id} not found.")
                return {"count": 0, "list": []}

            user_resume_links = await self.userResume_repo.get_all_by_user_id(user.id)
            if not user_resume_links:
                logger.debug(f"No resumes found for user {user_id}.")
                return {"count": 0, "list": []}

            resume_ids = [link.resume_id for link in user_resume_links]

            if not isinstance(resume_ids, list) or not resume_ids:
                return {"count": 0, "list": []}

            uploads: List[ResumeUploadModel] = await self.upload_repo.get_by_resume_id(
                resume_ids
            )

            upload_list = [
                {
                    "resume_id": upload.resume_id,
                    "filename": upload.filename,
                    "uploaded_at": str(upload.uploaded_at),
                    "status": "active" if upload.is_active else "inactive",
                }
                for upload in uploads
            ]
            logger.info(f"Found {len(uploads)} uploads for user {user_id}.")
            return {
                "count": len(upload_list),
                "list": upload_list,
            }

        except Exception as e:
            logger.error(
                f"Error retrieving resumes for user {user_id}: {str(e)}", exc_info=True
            )
            raise e
