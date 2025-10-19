"""
Pydantic schemas for User validation.
"""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserRead(BaseModel):
    """Schema for reading user data - NO password_hash!"""
    id: UUID
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True
