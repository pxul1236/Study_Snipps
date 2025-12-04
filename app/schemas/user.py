from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from uuid import UUID
from typing import Optional

#Base schema
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    university: Optional[str] = None

#Schema for creating a user(including password)
class UserCreate(UserBase):
    password: str = Field(..., min_length= 8)

#Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#Schema for returning user data(no password)
class UserResponse(UserBase):
    id: UUID
    is_admin: bool
    created_at: datetime
    class Config:
        from_attributes = True

#Schema for JWT response
class Token(BaseModel):
    access_token: str
    token_type: str

#Schmea for tokendata
class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    