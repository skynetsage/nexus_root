from datetime import datetime
import pytz
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile
from fastapi.responses import JSONResponse

from ..services.httpx_client import HttpxClient
from ..schemas.file import FileCreate, FileResponse, FileListResponse
from ..schemas.resume import ResumeCreate, ResumeUpdate
from ..db.postgres.repositories.file_repository import FileRepository
from ..db.postgres.repositories.resume_repository import ResumeRepository
from ..db.postgres.repositories.user_repository import UserRepository
from ..db.mongo.mongo import analysis_data, jd_data

from ..utils.file_util import upload_file, get_abs_path
from ..utils.resume_util import gen_custom_resume_id

from ..config.settings import settings

IST = pytz.timezone("Asia/Kolkata")


class ResumeController:
    def __init__(self, db: AsyncSession):
        self.file_repo = FileRepository(db)
        self.resume_repo = ResumeRepository(db)
        self.user_repo = UserRepository(db)

    async def upload_resume(self, user_id: int, file: UploadFile) -> FileResponse:
        try:
            user_data = await self.user_repo.get_user_by_id(user_id)
            if not user_data:
                raise HTTPException(status_code=404, detail="User not found")

            file_path = await upload_file(file)
            custom_id = gen_custom_resume_id(user_data.username)

            resume_entry = ResumeCreate(
                resume_id=custom_id, analysis_id=None, is_analyzed=False, is_active=True
            )
            await self.resume_repo.create_resume(resume_entry)

            file_entry = FileCreate(
                filename=file.filename,
                filepath=file_path,
                resume_id=custom_id,
                user_id=user_id,
                is_active=True,
            )
            res = await self.file_repo.create_file(file_entry)

            return FileResponse(
                id=res.id,
                filename=res.filename,
                filepath=res.filepath,
                resume_id=res.resume_id,
                user_id=res.user_id,
                is_active=res.is_active,
                created_at=res.created_at,
                updated_at=res.updated_at,
            )
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except FileNotFoundError as e:
            raise HTTPException(status_code=500, detail="File upload failed")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="An error occurred while processing the file"
            )

    async def get_all_resumes_for_user(
        self, user_id: int, limit: int = 10, offset: int = 0
    ) -> FileListResponse:
        try:
            user_data = await self.user_repo.get_user_by_id(user_id)
            if not user_data:
                raise HTTPException(status_code=404, detail="User not found")

            resume_list = await self.file_repo.get_all_by_user_id(
                user_id=user_id, limit=limit, offset=offset
            )

            if not resume_list:
                raise HTTPException(
                    status_code=404, detail="No resumes found for this user"
                )

            total_count = await self.file_repo.get_total_count_for_user_id(
                user_id=user_id
            )

            return FileListResponse(
                list=[
                    FileResponse(
                        id=res.id,
                        filename=res.filename,
                        filepath=res.filepath,
                        resume_id=res.resume_id,
                        user_id=res.user_id,
                        is_active=res.is_active,
                        created_at=res.created_at,
                        updated_at=res.updated_at,
                    )
                    for res in resume_list
                ],
                count=total_count,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    async def resume_analyze(self, user_id: int, jd: str):
        try:
            user_data = await self.user_repo.get_user_by_id(user_id)
            if not user_data:
                raise HTTPException(status_code=404, detail="User not found")

            file_data = await self.file_repo.get_file_by_user_id(user_id=user_id)
            if not file_data:
                raise HTTPException(
                    status_code=404, detail="No resume found for this user"
                )

            resume_data = await self.resume_repo.get_resume_by_resume_id_str(
                file_data.resume_id
            )
            if not resume_data:
                raise HTTPException(status_code=404, detail="Resume not found")
            json_payload = {
                "resume_id": resume_data.resume_id,
                "jd": jd,
                "file_path": get_abs_path(file_data.filepath),
            }

            client = HttpxClient(
                url=settings.AI_SERVICE_URL,
                method="POST",
                timeout=300.0,
                payload=json_payload,
            )
            response = await client.execute()

            jd_entry = await jd_data.insert_one(
                {
                    "jd": jd,
                    "created_at": datetime.now(IST),
                    "updated_at": datetime.now(IST),
                }
            )
            analysis_res = await analysis_data.insert_one(
                {
                    **response,
                    "created_at": datetime.now(IST),
                    "updated_at": datetime.now(IST),
                }
            )
            print("Analysis entry created in MongoDB:", analysis_res)
            await self.resume_repo.update_resume(
                resume_id=resume_data.resume_id,
                resume_update=ResumeUpdate(
                    analysis_id=str(analysis_res.inserted_id),
                    jd_id=str(jd_entry.inserted_id),
                    is_analyzed=True,
                ),
            )

            return JSONResponse(
                content={
                    "message": "Resume analysis completed successfully",
                    "analysis": response,
                    "analysis_id": str(analysis_res.inserted_id),
                    "jd_id": str(jd_entry.inserted_id),
                },
                status_code=200,
            )

        except HTTPException:
            raise
        except RuntimeError as re:
            raise HTTPException(
                status_code=500,
                detail=f"Failed send request to ai-service: {re}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while analyzing the resume: {e}",
            )
