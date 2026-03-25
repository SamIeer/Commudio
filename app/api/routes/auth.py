from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Annotated

from sqlalchemy.orm import Session
from app.core.database import get_db 

from app.schemas.user_schemas import CreateUser, UserResponse, LoginRequest, Token
from app.services.user_service import register_user, authenticate_create_token

from app.core.security import verify_password, hash_password, get_current_user
from app.repositories.user_repository import get_user_by_email

router = APIRouter(prefix="/auth")
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register", response_model=UserResponse)
def register_user_route(user_data: CreateUser,db: db_dependency):
    try:
        new_user = register_user(db,user_data)
        return new_user
    except ValueError:
        raise HTTPException(status_code=400, detail="Email already exists")
                
@router.post("/login", response_model=Token, summary="User login")
def login_user(login_data:LoginRequest, db:db_dependency):
    try:
        access_token = authenticate_create_token(db,login_data)
        return access_token
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@router.post("/recordings/")
async def upload_recording(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    try:
        contents = await file.read()
        return {"size": len(contents)}
    except error as e


