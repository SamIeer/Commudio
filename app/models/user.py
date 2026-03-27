from app.core.database import Base
from  sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, Enum, Text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True,nullable=False)
    full_name = Column(String)
    hashed_password = Column(String,nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # DateTime -> defines the column type, server_default=func.now()-> database automatically inserts the current timestamp when a record is created

class Recording(Base):
    __tablename__ = 'recordings'
    id = Column(Integer,primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    status  = Column(Enum("processing", "complete", "failed", name="status_enum"), default="processing") # (processing / complete / failed)
    transcript = Column(Text)
    filler_word_count = Column(Integer)
    words_per_minute = Column(Integer)
    feedback_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="recordings")