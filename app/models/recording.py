
from app.core.database import Base
from  sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, Enum, Text
from sqlalchemy.orm import relationship
from app.models.user import User

class Recording(Base):
    __tablename__ = 'recordings'
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    Recording_id = Column(Integer,primary_key=True, index=True)
    status  = Column(Enum("processing", "completed", "failed", name="status_enum"), default="processing") # (processing / complete / failed)
    transcript = Column(Text, nullable=True)
    filler_word_count = Column(Integer, nullable=True)
    words_per_minute = Column(Integer, nullable=True)
    feedback_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="recordings")