from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import Optional, List
from datetime import datetime

# Base model for common attributes
class UserBase(BaseModel):
    username: Optional[str] = Field(None, description="Username of the user")
    email: Optional[EmailStr] = Field(None, description="Email of the user")
    verified: bool = Field(False, description="Whether the user's email is verified")
    roles: Optional[List[str]] = Field(default_factory=list, description="List of roles assigned to the user")

    class Config:
        from_attributes = True  # Allows Pydantic to work with ORM models

# Schema for creating a new user (request body for POST)
class UserCreate(UserBase):
    password: SecretStr = Field(description="Password for the user")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email of the user")
    password: SecretStr = Field(..., description="Password of the user")


# Schema for updating an existing user (request body for PUT/PATCH)
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="New username")
    email: Optional[EmailStr] = Field(None, description="New email")
    verified: Optional[bool] = Field(None, description="Set verification status")
    password: Optional[SecretStr] = Field(None, description="New password for the user")
    roles: Optional[List[str]] = Field(None, description="Updated list of user roles")

# Schema for representing a user as it is in the database (includes DB-generated fields)
class UserInDBBase(UserBase):
    id: int = Field(description="Unique ID of the user")

class UserInDBBaseWithDate(UserBase):
    id: int = Field(description="Unique ID of the user")
    created_at: datetime = Field(description="Timestamp of user creation")
    updated_at: datetime = Field(description="Timestamp of last user update")

# Schema for a single user response (response body for GET by ID, POST, PUT)
class UserResponse(UserInDBBase):
    pass  # Password is not returned in the response

# Schema for a list of users, potentially with pagination info (response body for GET all)
class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(description="List of user objects")
    total: int = Field(description="Total number of users available")
    limit: Optional[int] = Field(None, description="The number of items per page")
    offset: Optional[int] = Field(None, description="The offset of the current page")
