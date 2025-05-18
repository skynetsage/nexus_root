from typing import Optional

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.postgres.models import ResumeModel
from app.schemas.resume_schema import ResumeCreate, ResumeRead, ResumeUpdate


class ResumeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_resume(self, resume_create: ResumeCreate) -> "ResumeRead":
        resume = ResumeModel(**resume_create.model_dump())
        self.db.add(resume)
        await self.db.commit()
        await self.db.refresh(resume)
        return ResumeRead.model_validate(resume)

    async def get_resume_by_resume_id(self, resume_id: str) -> Optional[ResumeModel]:
        result = await self.db.execute(
            select(ResumeModel).where(ResumeModel.resume_id == resume_id)
        )
        return result.scalars().first()

    async def update_resume(
        self, resume_id: str, resume_update: ResumeUpdate
    ) -> Optional[ResumeRead]:
        resume = await self.get_resume_by_resume_id(resume_id)
        if not resume:
            return None

        update_data = resume_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(resume, key, value)

        self.db.add(resume)
        await self.db.commit()
        await self.db.refresh(resume)

        return ResumeRead.model_validate(resume, from_attributes=True)

    async def get_all_resumes_by_user_id(self, user_id: int) -> list[ResumeRead]:
        result = await self.db.execute(
            select(ResumeModel)
            .options(selectinload(ResumeModel.file_upload))
            .where(ResumeModel.user_id == user_id)
        )
        resumes = result.scalars().all()
        return [ResumeRead.model_validate(resume) for resume in resumes]
