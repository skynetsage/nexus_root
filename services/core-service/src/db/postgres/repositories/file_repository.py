from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, Text
from sqlalchemy.orm import selectinload # For eager loading relationships if needed in the future

from ..models.file import FileTable
from ....schemas.file import FileCreate, FileUpdate # Assuming DTOs will be here


class FileRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_file(self, file_create: FileCreate) -> FileTable:
        """Create a new file record."""
        db_file = FileTable(**file_create.model_dump())
        self.db_session.add(db_file)
        await self.db_session.flush() # Use flush to get the ID before commit if needed elsewhere
        await self.db_session.refresh(db_file)
        return db_file

    async def get_file_by_id(self, file_id: int) -> Optional[FileTable]:
        query = select(FileTable).where(FileTable.id == file_id)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_all_files(self, limit: int = 100, offset: int = 0) -> List[FileTable]:
        """Get all files with pagination."""
        query = select(FileTable).offset(offset).limit(limit)
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def get_active_files(self, limit: int = 100, offset: int = 0) -> List[FileTable]:
        query = (
            select(FileTable)
            .where(FileTable.is_active == True)
            .offset(offset)
            .limit(limit)
        )
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def get_all_by_user_id(self, user_id: int, limit: int = 10, offset: int = 0) -> List[FileTable]:
        query = select(FileTable).where(FileTable.user_id == user_id).where(FileTable.is_active == True).offset(offset).limit(limit)
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def get_total_count_for_user_id(self, user_id: int) -> int:
        query =select(func.count()).select_from(FileTable).where(FileTable.user_id == user_id).where(FileTable.is_active == True)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none() or 0

    async def update_file(self, file_id: int, file_update: FileUpdate) -> Optional[FileTable]:
        db_file = await self.get_file_by_id(file_id)
        if not db_file:
            return None

        update_data = file_update.model_dump(exclude_unset=True)

        if not update_data:
            return db_file

        query = (
            update(FileTable)
            .where(FileTable.id == file_id)
            .values(**update_data)
            .returning(FileTable)
        )
        result = await self.db_session.execute(query)
        updated_file = result.scalars().first()
        if updated_file:
             for key, value in update_data.items():
                 setattr(db_file, key, value)
        return db_file

    async def delete_file(self, file_id: int) -> bool:
        query = delete(FileTable).where(FileTable.id == file_id)
        result = await self.db_session.execute(query)
        return result.rowcount > 0

    async def soft_delete_file(self, file_id: int) -> Optional[FileTable]:
        update_data = {"is_active": False}

        db_file = await self.get_file_by_id(file_id)
        if not db_file:
            return None

        query = (
            update(FileTable)
            .where(FileTable.id == file_id)
            .values(**update_data)
            .returning(FileTable)
        )
        result = await self.db_session.execute(query)
        updated_file = result.scalars().first()
        return updated_file

