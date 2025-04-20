from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.postgres.models import ResumeModel


class ResumeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> ResumeModel:
        result = await self.db.execute(select(ResumeModel).where(ResumeModel.id == id))
        return result.scalars().first()

    async def get_by_resume_id(self, resume_id: str) -> ResumeModel:
        result = await self.db.execute(
            select(ResumeModel).where(ResumeModel.resume_id == resume_id)
        )
        return result.scalars().first()

    async def create(self, resume: ResumeModel) -> ResumeModel:
        self.db.add(resume)
        await self.db.commit()
        await self.db.refresh(resume)
        return resume

    async def update(self, resume: ResumeModel) -> ResumeModel:
        await self.db.commit()
        await self.db.refresh(resume)
        return resume
