from fastapi import HTTPException, UploadFile
import tempfile

from sqlalchemy.orm import Session
from datetime import timedelta

from app.models.recording import Recording
from app.repositories.recording_repository import create_recording

# Dummy transcrpition function 
def transcribe_audio(file_path: str)-> str:
    return "transcribed text example"

def create_recording_service(db:Session,user_id: int,file: UploadFile):
    # checking if file is correct 
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not file.filename.endswith((".mp3",".wav",".m4a")):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    recording = create_recording(db, user_id)
    try: 
        with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as temp:
            temp.write(file.file.read())
            temp.flush()

            transcribe = transcribe_audio(temp.name)

        recording.transcript = transcribe
        recording.status = "complete"

        db.commit()
        db.refresh(recording)

        return Recording
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    new_recording = create_recording(db,user_id,file)

    return new_recording
    #if correct then we give the entrẏ of recording 
    # then return the recordings 
