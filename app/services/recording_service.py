import os 

from fastapi import HTTPException, UploadFile, BackgroundTasks
import tempfile

from sqlalchemy.orm import Session
from datetime import timedelta

from app.models.recording import Recording
from app.repositories.recording_repository import create_recording, update_recording

# Dummy transcrpition function 
def transcribe_audio(file_path: str)-> str:
    return "transcribed text example"
def get_fillers(transcribe:str)->int:
    return -1
def get_wpm(transcribe:str)->int:
    return -1

def process_recording(recording_id: int, file_path: str):
    db = SessionLocal() # Create New Session

    try:  
        transcript = transcribe_audio(file_path)
        filler_word_count = get_fillers(transcript)
        wpm = get_wpm(transcript)
        
        update_recording(
            db,
            recording_id,
            transcript=transcript,
            filler_word_count=filler_word_count,
            words_per_minute=wpm,
            status="completed"
        )

    except Exception as e:
        print("Processinģerror:", e)
        update_recording(
            db,
            recording_id,
            status="Failed"
        )
    finally:
        db.close()

        # Important Cleanup
        if os.exixts(file_path):
            os.remove(file_path)


async def create_recording_service(db:Session,user_id: int,file: UploadFile, background_tasks: BackgroundTasks):
    # checking if file is correct 
    recording = create_recording(db, user_id)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(file.file.read())
        temp_path = temp.name

    background_tasks.add_task(
        process_recording,
        recording.id,
        temp_path
    )
    
    return {
        "recording_id": recording.id,
        "status": "processing"
    }

    
