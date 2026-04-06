import os 
import openai 
import librosa

from fastapi import HTTPException, UploadFile, BackgroundTasks
import tempfile
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.recording import Recording
from app.repositories.recording_repository import create_recording, update_recording


# Dummy transcription function - replace with actual implementation later
def transcribe_audio(file_path: str) -> str:
    # """Placeholder for actual transcription service (Whisper, AssemblyAI, etc.)"""
    # return "transcribed text example"
    with open(file_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions("whisper-1", audio_file)
    return transcript


def get_fillers(transcript: str) -> int:
    # """Placeholder for filler word detection - implement with NLP"""
    # # TODO: Implement actual filler word counting (um, uh, like, etc.)
    # return 0
    filler_words = ['um', 'uh', 'like', 'you know', 'so', 'actually', 'basically']
    count = 0
    text_lower = transcript.lower()
    for filler in filler_words:
        count += text_lower.count(f"{filler}")
    return count

'''
You'll need to pass audio duration from transcription service 
Or calculate it seperately
'''
def get_audio_duration(file_path: str) -> float:
    duration = librosa.get_duration(path=file_path)
    return duration

def get_wpm(transcript: str, audio_duration_seconds: float) -> int:
    # """Placeholder for WPM calculation"""
    # # TODO: Implement actual WPM calculation based on audio duration
    # return 120
    word_count = len(transcript.split())
    duration_minutes = audio_duration_seconds / 60
    return int(word_count / duration_minutes) if duration_minutes > 0 else 0

def get_feedback(transcript: str) -> str:
    pass
def process_recording(recording_id: int, file_path: str):
    """Background task to process audio file"""
    db = SessionLocal()  # Create new session for background task

    try:  
        # Step 1: Transcribe audio
        transcript = transcribe_audio(file_path)
        
        # Step 2: Analyze transcript
        filler_word_count = get_fillers(transcript)
        wpm = get_wpm(transcript)

        # step 3: Feedback
        feedback = get_feedback(transcript)
        
        # Step 3: Update recording with results
        update_recording(
            db,
            recording_id,
            status="completed",
            transcript=transcript,
            filler_word_count=filler_word_count,
            words_per_minute=wpm,
            feedback_text=feedback
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