from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Base model for common attributes
class FileBase(BaseModel):
    filename: Optional[str] = Field(None, description="Name of the file")
    filepath: Optional[str] = Field(None, description="Path to the file")
    is_active: bool = Field(True, description="Whether the file is active")
    resume_id: Optional[int] = Field(None, description="ID of the associated resume")

    class Config:
        from_attributes = True #  Allows Pydantic to work with ORM models

# Schema for creating a new file (request body for POST)
class FileCreate(FileBase):
    pass # Inherits all fields from FileBase, all are relevant for creation

# Schema for updating an existing file (request body for PUT/PATCH)
# All fields are optional for updates
class FileUpdate(BaseModel):
    filename: Optional[str] = Field(None, description="New name of the file")
    filepath: Optional[str] = Field(None, description="New path to the file")
    is_active: Optional[bool] = Field(None, description="Set file active status")
    resume_id: Optional[int] = Field(None, description="New ID of the associated resume")

# Schema for representing a file as it is in the database (includes DB-generated fields)
class FileInDBBase(FileBase):
    id: int = Field(description="Unique ID of the file")
    created_at: datetime = Field(description="Timestamp of file creation")
    updated_at: datetime = Field(description="Timestamp of last file update")

# Schema for a single file response (response body for GET by ID, POST, PUT)
class FileResponse(FileInDBBase):
    pass #  This will be the standard representation sent to the client

# Schema for a list of files, potentially with pagination info (response body for GET all)
class FileListResponse(BaseModel):
    items: List[FileResponse] = Field(description="List of file objects")
    total: int = Field(description="Total number of files available")
    limit: Optional[int] = Field(None, description="The number of items per page")
    offset: Optional[int] = Field(None, description="The offset of the current page")

