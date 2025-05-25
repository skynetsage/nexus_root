from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ..models.resume import ResumeTable
from ....schemas.resume import ResumeCreate, ResumeUpdate

class ResumeRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_resume(self, resume_create: ResumeCreate) -> ResumeTable:
        db_resume = ResumeTable(**resume_create.model_dump())
        self.db_session.add(db_resume)
        await self.db_session.flush()
        await self.db_session.refresh(db_resume)
        return db_resume

    async def get_resume_by_id(self, resume_db_id: int) -> Optional[ResumeTable]:
        query = (
            select(ResumeTable)
            .where(ResumeTable.id == resume_db_id)
            .where(ResumeTable.is_active == True)
            .options(selectinload(ResumeTable.files))
        )
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_resume_by_resume_id_str(self, resume_id_str: str) -> Optional[ResumeTable]:
        query = (
            select(ResumeTable)
            .where(ResumeTable.resume_id == resume_id_str)
            .where(ResumeTable.is_active == True)
            .options(selectinload(ResumeTable.files))
        )
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_all_resumes(self, limit: int = 100, offset: int = 0) -> List[ResumeTable]:
        query = (
            select(ResumeTable)
            .offset(offset)
            .limit(limit)
            .options(selectinload(ResumeTable.files))
            .order_by(ResumeTable.id)
        )
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def update_resume(self, resume_db_id: int, resume_update: ResumeUpdate) -> Optional[ResumeTable]:
        """Update an existing resume by its internal database ID."""
        db_resume = await self.get_resume_by_id(resume_db_id) # Fetch first to ensure it exists
        if not db_resume:
            return None

        update_data = resume_update.model_dump(exclude_unset=True)
        if not update_data: # Nothing to update
            return db_resume # Return as is, no changes made

        query = (
            update(ResumeTable)
            .where(ResumeTable.id == resume_db_id)
            .values(**update_data)
            .returning(ResumeTable)
        )
        result = await self.db_session.execute(query)
        updated_instance_data = result.scalars().first()

        # Refresh the original instance with the updated data
        if updated_instance_data:
            for key, value in update_data.items():
                setattr(db_resume, key, value)
            # If your DB doesn't auto-update 'updated_at' via onupdate for some reason, or if you want to be explicit:
            # db_resume.updated_at = updated_instance_data.updated_at
            # However, SQLAlchemy's onupdate=func.now() should handle this.
            await self.db_session.refresh(db_resume, attribute_names=update_data.keys(), with_for_update=True)

        return db_resume

    async def delete_resume(self, resume_id: int) -> bool:
        query = delete(ResumeTable).where(ResumeTable.id == resume_id)
        result = await self.db_session.execute(query)
        return result.rowcount > 0

    async def soft_delete_resume(self, resume_id: int) -> Optional[ResumeTable]:
        update_data = {"is_active": False}
        existing = await self.get_resume_by_id(resume_id)
        if not existing:
            return None

        query = (
            update(ResumeTable)
            .where(ResumeTable.id == resume_id)
            .values(**update_data)
            .returning(ResumeTable)
        )
        res = await self.db_session.execute(query)
        updated_resume = res.scalars().first()
        return updated_resume

