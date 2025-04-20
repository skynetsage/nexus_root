from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ResumeUploadBase(BaseModel):
    resume_id: str
    filename: str
    file_path: str
    is_active: bool
    uploaded_at: datetime

    class Config:
        orm_mode = True  # Tells Pydantic to read data even if it's not a dict


class ResumeUploadCreate(ResumeUploadBase):
    pass


class ResumeUploadUpdate(ResumeUploadBase):
    filename: Optional[str] = None
    file_path: Optional[str] = None
    is_active: Optional[bool] = None


class ResumeUploadInDB(ResumeUploadBase):
    id: int
