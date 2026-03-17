from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from sqlalchemy.orm import Session
from app.core.database import get_db 

from app.schemas.user_schemas import CreateUser, UserResponse, LoginRequest
from app.services.user_service import register_user, authenticate_user

from app.core.security import verify_password, hash_password
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
                
@router.post("/login", response_model=UserResponse)
def log_in(login_data:LoginRequest, db:db_dependency):
    try:
        user = authenticate_user(db,LoginRequest)
        return user 
    except ValueError:
        raise HTTPException(status_code="401", detail="user not found")