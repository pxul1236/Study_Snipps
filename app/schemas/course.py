from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

# Base schema - shared fields
class CourseBase(BaseModel):
    course_code: str = Field(..., min_length=3, max_length=20)
    course_name: str = Field(..., min_length=3, max_length=200)
    department: str = Field(..., min_length=2, max_length=100)


# Schema for creating a course
class CourseCreate(CourseBase):
    pass

# Schema for updating a course (all fields optional)
class CourseUpdate(BaseModel):
    course_code: Optional[str] = Field(None, min_length=3, max_length=20)
    course_name: Optional[str] = Field(None, min_length=3, max_length=200)
    department: Optional[str] = Field(None, min_length=2, max_length=100)


# Schema for returning course data
class CourseResponse(CourseBase):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True