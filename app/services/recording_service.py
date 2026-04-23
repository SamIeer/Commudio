import os 
from app.core.config import settings

import json
from groq import Groq
import time
from faster_whisper import WhisperModel
import librosa

from fastapi import HTTPException, UploadFile, BackgroundTasks
import tempfile
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.recording import Recording
from app.repositories.recording_repository import create_recording, update_recording


MODE = "real"
# load model osnce (IMPORTANT for performance)


def get_model():
    model = None
    # global model
    if model is None:
        model = WhisperModel("base", compute_type="int8")
    return model


def transcribe_audio(file_path: str) -> str:
    if MODE == "mock":
        print("[MOCK] Using fake transcript")

        return """
        Hello this is a test recording.
        Um I am trying to check how my application works.
        Basically this should simulate real speech.
        """

    elif MODE == "real":
        print("[REAL] Transcribing audio...")

        model = get_model()

        segments, _ = model.transcribe(file_path)

        # combine all segments into one string
        full_text = " ".join([segment.text for segment in segments])

        return full_text.strip()
    


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


'''
Filler Function 
'''


def safe_parse_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None


client = Groq(api_key=settings.api_key)


def get_feedback(transcript: str, wpm: int, fillers: int) -> dict:
    # Optional safety trim (prevents huge prompts)
    transcript = transcript[:2000]
    prompt = f"""
    You are a communication coach with 50+ years of experience.

    Analyze the following speech:
    {transcript}

    Transcr
    - Filler words used: {fillers}
    - word per minutes: {wpm}

    Instructions:
    1. Provide exactly:
    - 2 bullet points for "good"
    - 2 bullet points for "bad"
    - 2 bullet points for "improve"
    - A short "overall" summary (2-3 lines)

    2. Keep feedback:
    - Clear and practical
    - Not generic
    - Based on the transcript and metrics

    3. Return ONLY valid JSON in this format:

    {{
    "good": ["...", "..."],
    "bad": ["...", "..."],
    "improve": ["...", "..."],
    "overall": "..."
    }}
    """
    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "Return ONLY valid JSON. No explanation. No markdown."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                top_p=0.9
            )

            text = response.choices[0].message.content.strip()

            # 🔧 Clean markdown if model adds it
            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            parsed = safe_parse_json(text)

            if parsed:
                return parsed

        except Exception as e:
            print(f"[ERROR][Attempt {attempt+1}] {e}")
            time.sleep(2)  # small backoff

    # 🔻 fallback response
    return {
        "good": [],
        "bad": [],
        "improve": [],
        "overall": "Could not generate feedback.",
        "scores": {
            "clarity": 0,
            "fluency": 0,
            "confidence": 0
        }
    }
    

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
        feedback = get_feedback(transcript, wpm, filler_word_count)

        # ✅ safe for DB
        feedback_json = json.dumps(feedback)   

        print(f"[STEP 4] Feedback generated")
        print(f"[DEBUG] Feedback preview: {feedback_json}...")

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
            feedback_text=feedback_json,
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
