from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.schemas.file_schema import FileRead


class ResumeCreate(BaseModel):
    resume_id: str
    user_id: int
    resume_analysis_id: str | None = None
    file_id: int


class ResumeUpdate(BaseModel):
    resume_id: Optional[str] = None
    user_id: Optional[int] = None
    resume_analysis_id: Optional[str] = None
    file_id: Optional[int] = None
    updated_at: Optional[datetime | None] = None


class ResumeRead(ResumeCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    File: Optional[FileRead] = None

    class Config:
        from_attributes = True
