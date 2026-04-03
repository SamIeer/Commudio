from fastapi import APIRouter,UploadFile, Depends
from app.core.security import get_current_user
from app.models.recording import Recording

rrecording = APIRouter()

@rrecording.post("/recordings/")
async def upload_recording(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)):
    content = await file.read()

    # create recoding entry 
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
