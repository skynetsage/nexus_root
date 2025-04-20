from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime


class ResumeBase(BaseModel):
    resume_analysis_id: Optional[UUID] = None
    resume_id: str
    overall_score: Optional[int] = None
    technical_score: Optional[int] = None
    grammer_score: Optional[int] = None
    is_analysed: Optional[bool] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ResumeCreate(ResumeBase):
    pass


class ResumeUpdate(ResumeBase):
    resume_analysis_id: Optional[UUID] = None
    overall_score: Optional[int] = None
    technical_score: Optional[int] = None
    grammer_score: Optional[int] = None
    is_analysed: Optional[bool] = None


class ResumeInDB(ResumeBase):
    id: int
