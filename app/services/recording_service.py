import os 
from openai import OpenAI
import librosa

from fastapi import HTTPException, UploadFile, BackgroundTasks
import tempfile
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.recording import Recording
from app.repositories.recording_repository import create_recording, update_recording


MODE = "mock"

def transcribe_audio(file_path: str) -> str:
    if MODE == "mock":
        print("[MOCK] Using fake transcript")

        return """
        Hello this is a test recording.
        Um I am trying to check how my application works.
        Basically this should simulate real speech.
        """

    elif MODE == "real":
        # plug OpenAI / Whisper / Gemini later
        pass



def get_fillers(transcript: str) -> int:
    # """Placeholder for filler word detection - implement with NLP"""
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
    # return 120
    word_count = len(transcript.split())
    duration_minutes = audio_duration_seconds / 60
    return int(word_count / duration_minutes) if duration_minutes > 0 else 0

def get_feedback(transcript: str,wpm:int) -> str:
    pass

def process_recording(
    recording_id: int,
    file_path: str,
    file_size: int = None,
    original_filename: str = None
):
    """Background task to process audio file with detailed debugging"""

    print(f"\n{'='*60}")
    print(f"🎯 BACKGROUND TASK STARTED")
    print(f"Recording ID: {recording_id}")
    print(f"File Path: {file_path}")
    print(f"Original Filename: {original_filename}")
    print(f"File Size: {file_size} bytes")
    print(f"{'='*60}\n")

    db = SessionLocal()

    try:
        # -------------------------------
        # STEP 0: Validate file exists
        # -------------------------------
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"[CHECK] File exists ✅")

        # -------------------------------
        # STEP 1: Get duration
        # -------------------------------
        duration = get_audio_duration(file_path)
        print(f"[STEP 1] Duration: {duration} seconds")

        # -------------------------------
        # STEP 2: Transcription
        # -------------------------------
        transcript = transcribe_audio(file_path)

        if not transcript:
            raise ValueError("Transcript is empty")

        print(f"[STEP 2] Transcription complete")
        print(f"[DEBUG] Transcript length: {len(transcript)} chars")
        print(f"[DEBUG] Preview: {transcript[:100]}...")

        # -------------------------------
        # STEP 3: Analysis
        # -------------------------------
        filler_word_count = get_fillers(transcript)
        wpm = get_wpm(transcript, duration)

        print(f"[STEP 3] Analysis complete")
        print(f"[DEBUG] Fillers: {filler_word_count}")
        print(f"[DEBUG] WPM: {wpm}")

        # -------------------------------
        # STEP 4: Feedback
        # -------------------------------
        feedback = get_feedback(transcript, wpm)

        print(f"[STEP 4] Feedback generated")
        print(f"[DEBUG] Feedback preview: {feedback}...")

        # -------------------------------
        # STEP 5: Update DB
        # -------------------------------
        print(f"[STEP 5] Updating database...")

        update_recording(
            db=db,
            recording_id=recording_id,
            transcript=transcript,
            filler_word_count=filler_word_count,
            words_per_minute=wpm,
            feedback_text=feedback,
            status="completed"
        )

        print(f"\n{'='*60}")
        print(f"✅ SUCCESS: Recording {recording_id} processed")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ ERROR processing recording {recording_id}")
        print(f"Error: {str(e)}")
        print(f"{'='*60}\n")

        import traceback
        traceback.print_exc()

        # Try marking as failed
        try:
            update_recording(db, recording_id, status="failed")
        except Exception as db_error:
            print(f"[ERROR] Failed to update DB status: {db_error}")

    finally:
        db.close()

        # -------------------------------
        # CLEANUP
        # -------------------------------
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"[CLEANUP] Temp file deleted: {file_path}")
        except Exception as cleanup_error:
            print(f"[CLEANUP ERROR] {cleanup_error}")


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
        recording.Recording_id,
        temp_path
    )
    
    return {
        "recording_id": recording.Recording_id,
        "status": "processing",
        "message": "Recording uploaded successfully. Processing in background."
    }