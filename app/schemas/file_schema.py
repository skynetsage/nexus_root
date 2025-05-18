from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class FileCreate(BaseModel):
    uploader_id: int
    filename: str
    file_path: str
    is_active: bool = True


class FileUpdate(BaseModel):
    filename: Optional[str] = None
    file_path: Optional[str] = None
    is_active: Optional[bool] = None
    updated_at: Optional[datetime | None] = None


class FileRead(FileCreate):
    id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True
