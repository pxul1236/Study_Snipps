from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from uuid import UUID
from typing import Optional

# Base schema - shared fields
class NoteBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    file_url: str  # URL to uploaded file (Cloudinary/S3)
    file_type: str = Field(..., pattern="^(pdf|image|png|jpg|jpeg)$")
    course_id: UUID

# Schema for creating a note
class NoteCreate(NoteBase):
    pass

# Schema for updating a note (all fields optional except course_id)
class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    file_url: Optional[str] = None
    file_type: Optional[str] = Field(None, pattern="^(pdf|image|png|jpg|jpeg)$")

# Schema for returning note data
class NoteResponse(NoteBase):
    id: UUID
    uploaded_by: UUID
    upvotes_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Schema for note with uploader info
class NoteWithUploader(NoteResponse):
    uploader_name: str  # First + Last name of uploader
    uploader_email: str