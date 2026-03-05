from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    username: str
    

class CreateUser(UserBase):
    password: str
    confirm_password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

