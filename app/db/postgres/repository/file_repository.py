from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.postgres.models import FileUploadModel
from app.schemas.file_schema import FileCreate, FileRead


class FileUploadRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, file_create: FileCreate) -> FileRead:
        file = FileUploadModel(**file_create.model_dump())
        self.db.add(file)
        await self.db.commit()
        await self.db.refresh(file)
        return FileRead.model_validate(file)

    async def get_file_by_id(self, file_id: int) -> FileRead | None:
        result = await self.db.execute(
            select(FileUploadModel).where(FileUploadModel.id == file_id)
        )
        return result.scalars().first()
