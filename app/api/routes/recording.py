from app.models.user import User
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.recording import Recording

from app.core.database import get_db
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
        "recording_id": recording.Recording_id,
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
                "id": rec.Recording_id,
                "status": rec.status,
                "transcript": rec.transcript,
                "filler_word_count": rec.filler_word_count,
                "words_per_minute": rec.words_per_minute,
                "feedback_text": rec.feedback_text,
                "created_at": rec.created_at
            }
            for rec in recordings
        ]
    }


'''
Added Part from 
'''

@recording.delete("/recordings/{recording_id}", summary="Delete recording")
async def delete_recording(
    recording_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a recording permanently.
    
    This will remove the recording from the database.
    In V2, this will also delete the audio file from storage.
    """
    rec = get_recording_by_id(db, recording_id, current_user.id)
    
    if not rec:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    # Delete from database
    db.delete(rec)
    db.commit()
    
    # TODO V2: Delete from S3/storage if audio_url exists
    
    return {
        "message": "Recording deleted successfully",
        "recording_id": recording_id
    }


@recording.get("/recordings/stats/summary", summary="Get user statistics")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get aggregate statistics for all user recordings.
    
    Returns averages, totals, and trends for dashboard display.
    """
    recordings = get_user_recordings(db, current_user.id, skip=0, limit=1000)
    
    # Filter only completed recordings for stats
    completed = [r for r in recordings if r.status == "completed"]
    
    if not completed:
        return {
            "total_recordings": len(recordings),
            "completed_recordings": 0,
            "processing_recordings": len([r for r in recordings if r.status == "processing"]),
            "failed_recordings": len([r for r in recordings if r.status == "failed"]),
            "average_wpm": 0,
            "average_filler_count": 0,
            "total_practice_time_minutes": 0
        }
    
    # Calculate averages
    avg_wpm = sum(r.words_per_minute or 0 for r in completed) / len(completed)
    avg_fillers = sum(r.filler_word_count or 0 for r in completed) / len(completed)
    total_time = sum(r.duration_seconds or 0 for r in completed)
    
    return {
        "total_recordings": len(recordings),
        "completed_recordings": len(completed),
        "processing_recordings": len([r for r in recordings if r.status == "processing"]),
        "failed_recordings": len([r for r in recordings if r.status == "failed"]),
        "average_wpm": round(avg_wpm, 1),
        "average_filler_count": round(avg_fillers, 1),
        "total_practice_time_minutes": round(total_time / 60, 1)
    }


@recording.get("/recordings/stats/trend", summary="Get performance trend")
async def get_performance_trend(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get performance trend over time (for charts in V3 frontend).
    
    Returns chronological data for WPM and filler words.
    """
    recordings = get_user_recordings(db, current_user.id, skip=0, limit=1000)
    completed = [r for r in recordings if r.status == "completed"]
    
    # Sort by date
    completed.sort(key=lambda x: x.created_at)
    
    trend_data = [
        {
            "recording_id": rec.Recording_id,
            "date": rec.created_at.isoformat(),
            "wpm": rec.words_per_minute,
            "filler_count": rec.filler_word_count,
            "duration": rec.duration_seconds
        }
        for rec in completed
    ]
    
    return {
        "trend": trend_data,
        "total_points": len(trend_data)
    }