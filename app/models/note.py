from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

class Note(Base):
    __tablename__ = "notes"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    #note fields
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    file_url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    
    #upvotes
    #upvotes_count = Column(Integer, default=0, server_default='0', nullable=False)

    #Foreign key
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    #Timestamps for creation/updation
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable= False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    #Relationships
    uploader = relationship("User", backref="uploaded_notes")
    course = relationship("Course", back_populates="notes")