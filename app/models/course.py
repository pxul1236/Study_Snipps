from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    #course fields
    course_code = Column(String, unique=True, nullable=False, index=True)
    course_name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    
    #Foreign key
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    #Timestamps for creation/updation
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable= False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    #Relationships
    creator = relationship("User", backref="courses")
    notes = relationship("Note", back_populates="course", cascade="all, delete-orphan")