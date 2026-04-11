# from fastapi
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class RecordingResponse(BaseModel):
    id: int
    status: str
    transcript: str | None
    filler_word_count: int | None
    words_per_minute: int | None

    class Config:
        from_attributes = True