from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserResumeBase(BaseModel):
    resume_id: str
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Tells Pydantic to read data even if it's not a dict


class UserResumeCreate(UserResumeBase):
    pass


class UserResumeUpdate(UserResumeBase):
    resume_id: Optional[str] = None
    user_id: Optional[int] = None


class UserResumeInDB(UserResumeBase):
    id: int
