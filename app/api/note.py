from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from app.database import get_db
from app.models.note import Note
from app.models.course import Course
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse, NoteWithUploader
from app.utils.auth import get_current_user

router = APIRouter(tags=["Note"])


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def upload_note(
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Any authenticated user!
):
    """Upload a new note to a course (Any authenticated user)."""
    
    # Verify course exists
    course = db.query(Course).filter(Course.id == note_data.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Create new note
    new_note = Note(
        title=note_data.title,
        description=note_data.description,
        file_url=note_data.file_url,
        file_type=note_data.file_type,
        course_id=note_data.course_id,
        uploaded_by=current_user.id
    )
    
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    
    return new_note


@router.get("/", response_model=List[NoteWithUploader])
def get_all_notes(
    db: Session = Depends(get_db),
    course_id: Optional[UUID] = Query(None, description="Filter by course"),
    search: Optional[str] = Query(None, description="Search note titles"),
    sort_by: str = Query("recent", regex="^(recent|popular)$", description="Sort by recent or popular"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Get all notes with optional filters (Public access)."""
    
    query = db.query(Note, User).join(User, Note.uploaded_by == User.id)
    
    # Apply filters
    if course_id:
        query = query.filter(Note.course_id == course_id)
    
    if search:
        query = query.filter(Note.title.ilike(f"%{search}%"))
    
    # Sorting
    if sort_by == "popular":
        query = query.order_by(Note.upvotes_count.desc())
    else:  # recent
        query = query.order_by(Note.created_at.desc())
    
    # Pagination
    results = query.offset(skip).limit(limit).all()
    
    # Format response with uploader info
    notes_with_uploader = []
    for note, user in results:
        note_dict = {
            "id": note.id,
            "title": note.title,
            "description": note.description,
            "file_url": note.file_url,
            "file_type": note.file_type,
            "course_id": note.course_id,
            "uploaded_by": note.uploaded_by,
            #"upvotes_count": note.upvotes_count,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
            "uploader_name": f"{user.first_name} {user.last_name}",
            "uploader_email": user.email
        }
        notes_with_uploader.append(note_dict)
    
    return notes_with_uploader


@router.get("/{note_id}", response_model=NoteWithUploader)
def get_note_by_id(
    note_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a single note by ID (Public access)."""
    
    result = db.query(Note, User).join(User, Note.uploaded_by == User.id).filter(Note.id == note_id).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    note, user = result
    
    return {
        "id": note.id,
        "title": note.title,
        "description": note.description,
        "file_url": note.file_url,
        "file_type": note.file_type,
        "course_id": note.course_id,
        "uploaded_by": note.uploaded_by,
        #"upvotes_count": note.upvotes_count,
        "created_at": note.created_at,
        "updated_at": note.updated_at,
        "uploader_name": f"{user.first_name} {user.last_name}",
        "uploader_email": user.email
    }


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: UUID,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a note (Only note owner can update)."""
    
    note = db.query(Note).filter(Note.id == note_id).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    # Check if current user is the owner
    if note.uploaded_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own notes"
        )
    
    # Update only provided fields
    update_data = note_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(note, key, value)
    
    db.commit()
    db.refresh(note)
    
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a note (Owner or Admin can delete)."""
    
    note = db.query(Note).filter(Note.id == note_id).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    # Check if current user is owner OR admin
    if note.uploaded_by != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own notes"
        )
    
    db.delete(note)
    db.commit()
    
    return None