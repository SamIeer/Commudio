from fastapi import BackgroundTasks,APIRouter,UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.models.recording import Recording
from app.services.recording_service import create_recording_service

rrecording = APIRouter()

MAX_FILE_SIZE = 25*1024*1024
ALLOWED_TYPES = (".mp4",".wav", ".m4a")

@rrecording.post("/recordings")
async def upload_recording(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks
):
    return await create_recording_service(
        db=db,
        user_id=current_user.id,
        file=file,
        background_tasks=background_tasks
    )


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