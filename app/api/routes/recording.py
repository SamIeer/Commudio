from fastapi import APIRouter,UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.models.recording import Recording

rrecording = APIRouter()

MAX_FILE_SIZE = 25*1024*1024
ALLOWED_TYPES = (".mp4",".wav", ".m4a")

@rrecording.post("/recordings/")
async def upload_recording(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)):

    # read file
    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    # create recoding entry #
    recording = Recording(
        user_id = current_user.id,
        status = "processing"
    ) # set status'

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "user_id": current_user.id
    }


@router.get("/recordings/{recording_id}")
def get_recording(
    recording_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_recording_service(
        db,
        current_user.id,
        recording_id
    )