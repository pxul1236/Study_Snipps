from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from app.database import get_db
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.utils.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/course", tags=["Course"])


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)  # Only admins!
):
    """Create a new course (Admin only)."""
    
    # Check if course code already exists
    existing_course = db.query(Course).filter(Course.course_code == course_data.course_code).first()
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course with code '{course_data.course_code}' already exists"
        )
    
    # Create new course
    new_course = Course(
        course_code=course_data.course_code,
        course_name=course_data.course_name,
        department=course_data.department,
        created_by=current_admin.id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    return new_course

@router.get("/", response_model=List[CourseResponse])
def get_all_courses(
    db: Session = Depends(get_db),
    department: Optional[str] = Query(None, description="Filter by department"),
    search: Optional[str] = Query(None, description="Search course name or code"),
    skip: int = Query(0, ge=0, description="Number of courses to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max courses to return")
):
    """Get all courses with optional filters (Public access)."""
    
    query = db.query(Course)
    
    # Apply filters
    if department:
        query = query.filter(Course.department.ilike(f"%{department}%"))
    
    
    if search:
        query = query.filter(
            (Course.course_name.ilike(f"%{search}%")) |
            (Course.course_code.ilike(f"%{search}%"))
        )
    
    # Pagination
    courses = query.offset(skip).limit(limit).all()
    
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
def get_course_by_id(
    course_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a single course by ID (Public access)."""
    
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: UUID,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)  # Only admins!
):
    """Update a course (Admin only)."""
    
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Update only provided fields
    update_data = course_data.model_dump(exclude_unset=True)
    
    # Check if updating course_code and it conflicts with existing
    if "course_code" in update_data:
        existing = db.query(Course).filter(
            Course.course_code == update_data["course_code"],
            Course.id != course_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Course with code '{update_data['course_code']}' already exists"
            )
    
    for key, value in update_data.items():
        setattr(course, key, value)
    
    db.commit()
    db.refresh(course)
    
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)  # Only admins!
):
    """Delete a course (Admin only). This will also delete all notes in this course."""
    
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    db.delete(course)
    db.commit()
    
    return None