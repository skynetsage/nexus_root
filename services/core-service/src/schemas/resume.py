from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from ..schemas.file import FileResponse

class ResumeBase(BaseModel):
    resume_id: str = Field(description="External unique identifier for the resume")
    analysis_id: Optional[str] = Field(None, description="Identifier for an analysis associated with the resume")
    is_analyzed: bool = Field(False, description="Whether the resume has been analyzed")
    is_active: bool = Field(True, description="Whether the resume is active")
    class Config:
        from_attributes = True

#(request body for POST)
class ResumeCreate(ResumeBase):
    pass

# (request body for PUT/PATCH)
# All fields are optional for updates
class ResumeUpdate(BaseModel):
    resume_id: Optional[str] = Field(None, description="New external unique identifier for the resume")
    analysis_id: Optional[str] = Field(None, description="New identifier for an analysis")
    is_analyzed: Optional[bool] = Field(None, description="Set resume analyzed status")
    is_active: Optional[bool] = Field(None, description="Set resume active status")

class ResumeInDBBase(ResumeBase):
    id: int = Field(description="Internal unique ID of the resume")
    created_at: datetime = Field(description="Timestamp of resume record creation")
    updated_at: datetime = Field(description="Timestamp of last resume record update")

# (response body for GET by ID, POST, PUT)
class ResumeResponse(ResumeInDBBase):
    files: List[FileResponse] = Field([], description="List of files associated with this resume")

# Schema for a list of resumes, potentially with pagination info (response body for GET all)
class ResumeListResponse(BaseModel):
    items: List[ResumeResponse] = Field(description="List of resume objects")
    total: int = Field(description="Total number of resumes available")
    limit: Optional[int] = Field(None, description="The number of items per page")
    offset: Optional[int] = Field(None, description="The offset of the current page")

