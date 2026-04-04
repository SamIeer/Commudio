import os 
from fastapi import HTTPException, UploadFile, BackgroundTasks
import tempfile
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.recording import Recording
from app.repositories.recording_repository import create_recording, update_recording


# Dummy transcription function - replace with actual implementation later
def transcribe_audio(file_path: str) -> str:
    """Placeholder for actual transcription service (Whisper, AssemblyAI, etc.)"""
    return "transcribed text example"


def get_fillers(transcript: str) -> int:
    """Placeholder for filler word detection - implement with NLP"""
    # TODO: Implement actual filler word counting (um, uh, like, etc.)
    return 0


def get_wpm(transcript: str) -> int:
    """Placeholder for WPM calculation"""
    # TODO: Implement actual WPM calculation based on audio duration
    return 120


def process_recording(recording_id: int, file_path: str):
    """Background task to process audio file"""
    db = SessionLocal()  # Create new session for background task

    try:  
        # Step 1: Transcribe audio
        transcript = transcribe_audio(file_path)
        
        # Step 2: Analyze transcript
        filler_word_count = get_fillers(transcript)
        wpm = get_wpm(transcript)
        
        # Step 3: Update recording with results
        update_recording(
            db,
            recording_id,
            transcript=transcript,
            filler_word_count=filler_word_count,
            words_per_minute=wpm,
            status="completed"
        )
        print(f"Successfully processed recording {recording_id}")

    except Exception as e:
        print(f"Processing error for recording {recording_id}:", e)
        update_recording(
            db,
            recording_id,
            status="failed"
        )
    finally:
        db.close()
        
        # Important: Cleanup temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Cleaned up temp file: {file_path}")


async def create_recording_service(
    db: Session, 
    user_id: int, 
    file: UploadFile, 
    background_tasks: BackgroundTasks
):
    """Main service to handle recording upload and processing"""
    
    # Validate file type
    if not file.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.mp4')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Allowed: mp3, wav, m4a, mp4"
        )
    
    # Create recording entry in database
    recording = create_recording(db, user_id)
    
    # Save uploaded file to temporary location
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            content = await file.read()
            temp.write(content)
            temp_path = temp.name
    except Exception as e:
        # If file saving fails, update status and cleanup
        update_recording(db, recording.id, status="failed")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Add background task to process the recording
    background_tasks.add_task(
        process_recording,
        recording.id,
        temp_path
    )
    
    return {
        "recording_id": recording.id,
        "status": "processing",
        "message": "Recording uploaded successfully. Processing in background."
    }