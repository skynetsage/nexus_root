from collections import defaultdict
from typing import List, Optional, Tuple, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, case
from sqlalchemy.orm import selectinload

from ..models.resume import ResumeTable
from ..models.file import FileTable
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

    async def get_resume_by_resume_id_str(
        self, resume_id_str: str
    ) -> Optional[ResumeTable]:
        query = (
            select(ResumeTable)
            .where(ResumeTable.resume_id == resume_id_str)
            .where(ResumeTable.is_active == True)
            .options(selectinload(ResumeTable.files))
        )
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_all_resumes(
        self, limit: int = 100, offset: int = 0
    ) -> List[ResumeTable]:
        query = (
            select(ResumeTable)
            .offset(offset)
            .limit(limit)
            .options(selectinload(ResumeTable.files))
            .order_by(ResumeTable.id)
        )
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def update_resume(
        self, resume_id: str, resume_update: ResumeUpdate
    ) -> Optional[ResumeTable]:
        """Update an existing resume by its internal database ID."""
        db_resume = await self.get_resume_by_resume_id_str(resume_id)
        if not db_resume:
            return None

        update_data = resume_update.model_dump(exclude_unset=True)
        if not update_data:  # Nothing to update
            return db_resume  # Return as is, no changes made

        query = (
            update(ResumeTable)
            .where(ResumeTable.resume_id == resume_id)
            .values(**update_data)
            .returning(ResumeTable)
        )
        result = await self.db_session.execute(query)
        updated_instance_data = result.scalars().first()

        if updated_instance_data:
            for key, value in update_data.items():
                setattr(db_resume, key, value)
            await self.db_session.refresh(
                db_resume, attribute_names=update_data.keys(), with_for_update=True
            )

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

    async def get_resume_counts_by_user_id(self, user_id: int) -> dict:
        stmt = (
            select(
                func.count(ResumeTable.id).label("total_resumes"),
                func.count(case((ResumeTable.is_active == True, 1))).label(
                    "active_resumes"
                ),
                func.count(case((ResumeTable.is_active == False, 1))).label(
                    "inactive_resumes"
                ),
                func.count(case((ResumeTable.is_analyzed == True, 1))).label(
                    "analyzed_resumes"
                ),
                func.count(case((ResumeTable.is_analyzed == False, 1))).label(
                    "unanalyzed_resumes"
                ),
            )
            .join(FileTable, ResumeTable.resume_id == FileTable.resume_id)
            .where(FileTable.user_id == user_id)
        )

        result = await self.db_session.execute(stmt)
        row = result.one()

        return {
            "total_resumes": row.total_resumes,
            "active_resumes": row.active_resumes,
            "inactive_resumes": row.inactive_resumes,
            "analyzed_resumes": row.analyzed_resumes,
            "unanalyzed_resumes": row.unanalyzed_resumes,
        }

    async def get_all_resumes_by_user_id(self, user_id: int) -> List[ResumeTable]:
        query = (
            select(ResumeTable)
            .join(FileTable, ResumeTable.resume_id == FileTable.resume_id)
            .where(FileTable.user_id == user_id)
            .where(ResumeTable.is_active == True)
            .where(ResumeTable.is_analyzed == True)
            .options(selectinload(ResumeTable.files))
        )
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def get_latest_resume_by_user_id(self, user_id: int) -> Optional[ResumeTable]:
        query = (
            select(ResumeTable)
            .join(FileTable, ResumeTable.resume_id == FileTable.resume_id)
            .where(FileTable.user_id == user_id)
            .where(ResumeTable.is_active == True)
            .order_by(ResumeTable.created_at.desc())
            .limit(1)
            .options(selectinload(ResumeTable.files))
        )
        result = await self.db_session.execute(query)
        return result.scalars().first() if result else None

    async def get_monthly_resume_counts(
        self, user_id: int
    ) -> Tuple[Dict[str, Dict[str, int]], Dict[str, str]]:
        stmt = (
            select(ResumeTable)
            .join(FileTable, ResumeTable.resume_id == FileTable.resume_id)
            .where(ResumeTable.is_active == True)
            .where(FileTable.user_id == user_id)
        )

        result = await self.db_session.execute(stmt)
        resumes = result.scalars().all()

        monthly_counts = defaultdict(lambda: {"total_uploaded": 0, "total_analyzed": 0})
        analysis_id_to_month = {}

        for resume in resumes:
            month_key = resume.created_at.strftime("%Y-%m")
            monthly_counts[month_key]["total_uploaded"] += 1

            if resume.analysis_id:
                monthly_counts[month_key]["total_analyzed"] += 1
                analysis_id_to_month[resume.analysis_id] = month_key

        return monthly_counts, analysis_id_to_month
