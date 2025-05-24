from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
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
        """Get a single file by its ID."""
        query = select(FileTable).where(FileTable.id == file_id)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_files_by_resume_id(self, resume_id: int, limit: int = 100, offset: int = 0) -> List[FileTable]:
        """Get all files associated with a specific resume_id, with pagination."""
        query = (
            select(FileTable)
            .where(FileTable.resume_id == resume_id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def get_all_files(self, limit: int = 100, offset: int = 0) -> List[FileTable]:
        """Get all files with pagination."""
        query = select(FileTable).offset(offset).limit(limit)
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def get_active_files(self, limit: int = 100, offset: int = 0) -> List[FileTable]:
        """Get all active files with pagination."""
        query = (
            select(FileTable)
            .where(FileTable.is_active == True)
            .offset(offset)
            .limit(limit)
        )
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def update_file(self, file_id: int, file_update: FileUpdate) -> Optional[FileTable]:
        """Update an existing file by its ID."""
        # Fetch the file first to ensure it exists
        db_file = await self.get_file_by_id(file_id)
        if not db_file:
            return None

        # Get data to update, excluding unset values to avoid overwriting with None
        update_data = file_update.model_dump(exclude_unset=True)

        if not update_data: # Nothing to update
            return db_file

        query = (
            update(FileTable)
            .where(FileTable.id == file_id)
            .values(**update_data)
            .returning(FileTable) # Return the updated row
        )
        result = await self.db_session.execute(query)
        # await self.db_session.flush() # Not strictly necessary with returning() but good for consistency
        # await self.db_session.refresh(db_file) # refresh might not work as expected after returning
        updated_file = result.scalars().first()
        if updated_file: # if returning worked, refresh the original instance with new data
             for key, value in update_data.items():
                 setattr(db_file, key, value)
             # Manually update updated_at if not handled by onupdate in all scenarios or if you want to be explicit
             # db_file.updated_at = datetime.utcnow() # Or use func.now() if appropriate for your DB timezone settings
        return db_file # Return the original instance, now updated

    async def delete_file(self, file_id: int) -> bool:
        """Delete a file by its ID (hard delete)."""
        query = delete(FileTable).where(FileTable.id == file_id)
        result = await self.db_session.execute(query)
        # await self.db_session.flush()
        return result.rowcount > 0

    async def soft_delete_file(self, file_id: int) -> Optional[FileTable]:
        """Soft delete a file by its ID (sets is_active to False)."""
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
        # await self.db_session.flush()
        updated_file = result.scalars().first()
        if updated_file:
            db_file.is_active = False # Update the instance
            # db_file.updated_at = datetime.utcnow() # Or func.now()
        return db_file

