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

