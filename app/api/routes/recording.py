from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.recording import Recording

from app.core.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.services.recording_service import create_recording_service
from app.repositories.recording_repository import get_recording_by_id, get_user_recordings

recording = APIRouter()

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB
ALLOWED_TYPES = (".mp3", ".wav", ".m4a", ".mp4")


@recording.post("/recordings/")
async def upload_recording(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Upload audio recording for transcription and analysis"""
    
    # Validate file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max 25MB allowed.")
    
    # Reset file pointer for service layer
    await file.seek(0)
    
    # Validate file type
    if not file.filename.lower().endswith(ALLOWED_TYPES):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_TYPES)}"
        )
    
    # Use service layer to handle recording creation
    result = await create_recording_service(
        db=db,
        user_id=current_user.id,
        file=file,
        background_tasks=background_tasks
    )
    
    return result

@recording.get("/recordings/{recording_id}")
async def get_recording(
    recording_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific recording by ID"""
    recording = get_recording_by_id(db, recording_id, current_user.id)
    
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    return {
        "id": recording.id,
        "status": recording.status,
        "transcript": recording.transcript,
        "filler_word_count": recording.filler_word_count,
        "words_per_minute": recording.words_per_minute,
        "feedback_text": recording.feedback_text,
        "created_at": recording.created_at
    }


@recording.get("/recordings/")
async def list_recordings(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all recordings for the current user"""
    recordings = get_user_recordings(db, current_user.id, skip, limit)
    
    return {
        "total": len(recordings),
        "recordings": [
            {
                "id": rec.id,
                "status": rec.status,
                "created_at": rec.created_at,
                "filler_word_count": rec.filler_word_count,
                "words_per_minute": rec.words_per_minute
            }
            for rec in recordings
        ]
    }