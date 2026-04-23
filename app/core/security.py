import os 
from app.core.config import settings
from fastapi import Depends, HTTPException, status

from app.schemas.user_schemas import LoginRequest
from  sqlalchemy.orm import Session
from app.repositories.user_repository import get_user_by_email, get_user_by_id
from app.core.database import get_db
from typing import Annotated

from jose import JWTError,jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer



pwd_context = CryptContext(
    schemes = ['argon2'],
    deprecated="auto" )

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# python -c "import secrets; print(secrets.token_hex(32))"
def create_access_token(user_id: int, expires_delta: timedelta = timedelta(minutes=120))->str:
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    to_encode = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp" : int(expire.timestamp())
    }  # Use the provided data
    return jwt.encode(to_encode, settings.secret_key, settings.algorithm)

# Decoding the token 
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token: Annotated[str, Depends(oauth2_bearer)],db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm]) # verifies the token's signature and decodes its contents
        user_id: str = payload.get("sub")  # Extract the user_id
        if user_id is None:
            raise  HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"})
        
        user = get_user_by_id(db,int(user_id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"})
        return user 
        
    except JWTError:
            raise  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"})

