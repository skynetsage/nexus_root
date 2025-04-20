from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from app.db.postgres.models import UserResumeModel


class UserResumeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> UserResumeModel:
        result = await self.db.execute(
            select(UserResumeModel).where(UserResumeModel.id == id)
        )
        return result.scalars().first()

    async def get_by_user_id_and_resume_id(
        self, user_id: str, resume_id: str
    ) -> UserResumeModel:
        result = await self.db.execute(
            select(UserResumeModel).where(
                UserResumeModel.user_id == user_id,
                UserResumeModel.resume_id == resume_id,
            )
        )
        return result.scalars().first()

    async def get_all_by_user_id(self, user_id: int) -> list[UserResumeModel]:
        result = await self.db.execute(
            select(UserResumeModel)
            .where(UserResumeModel.user_id == user_id)
            .options(joinedload(UserResumeModel.resume))
        )
        return result.scalars().all()

    async def create(self, user_resume: UserResumeModel) -> UserResumeModel:
        self.db.add(user_resume)
        await self.db.commit()
        await self.db.refresh(user_resume)
        return user_resume
