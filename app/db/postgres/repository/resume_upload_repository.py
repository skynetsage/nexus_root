from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.postgres.models import ResumeUploadModel


class ResumeUploadRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> ResumeUploadModel:
        result = await self.db.execute(
            select(ResumeUploadModel).where(ResumeUploadModel.id == id)
        )
        return result.scalars().first()

    async def get_by_resume_id(self, resume_id: list[str]) -> list[ResumeUploadModel]:
        result = await self.db.execute(
            select(ResumeUploadModel).where(ResumeUploadModel.resume_id.in_(resume_id))
        )
        return result.scalars().all()

    async def create(self, resume_upload: ResumeUploadModel) -> ResumeUploadModel:
        self.db.add(resume_upload)
        await self.db.commit()
        await self.db.refresh(resume_upload)
        return resume_upload

    async def soft_delete(self, resume_upload: ResumeUploadModel) -> None:
        resume_upload.is_active = False
        await self.db.commit()
