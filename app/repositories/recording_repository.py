from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.recording import Recording

def create_recording(db:Session,user_id)->Recording:
    try:
        recording = Recording(
            user_id = user_id,
            status = "processing"
        )
        db.add(recording)
        db.commit()
        db.refresh(recording)

        return recording
    except Exception as e:
        db.rollback()
        raise e 

def update_recording(db:Session,recording_id: int,
                    transcript: str | None = None,
                    filler_word_count: int | None = None,
                    words_per_minute: int | None = None,
                    feedback_text: str | None = None,
                    status: str | None = None) -> Recording:
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    if not recording:
        raise ValueError("Recording not found")
    
    # Update only provided fields 
    if transcript is not None:
        recording.filler_word_cound = filler_word_count
    
    if filler_word_count is not None:
        recording.filler_wprd_count = filler_word_count
    
    if words_per_minute is not None:
        recording.words_per_minute = words_per_minute

    if feedback_text is not None:
        recording.feedback_text = feedback_text

    if status is not None:
        recording.status = status

    db.commit()
    db.refresh(recording)

    return recording
