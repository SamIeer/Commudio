from sqlalchemy.orm import Session
from datetime import timedelta

from app.schemas.user_schemas import CreateUser, UserResponse, LoginRequest, Token
from app.repositories import user_repository as user_repo
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User

'''why this architecture for tje real production system'''
'''
What the service should receive 
-> db: Session - so it can call the repository, need to interact with repo
-> user_data: CreateUser - schema from the API layer, comes from API validation layer
What the service should return 
-> UserResponse (or UserRead) - a response schema, not ORM
'''
def register_user(db: Session, user_data: CreateUser) -> UserResponse:
    existing_user= user_repo.get_user_by_email(db, user_data.email)
    if existing_user:
        raise ValueError("Email already registered")
    
    hashed_password = hash_password(user_data.password)

    user = user_repo.create_user(
        db,
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
    )
    return UserResponse.model_validate(user)

def authenticate_user(db:Session, login_data:LoginRequest)-> User: #ORM:
    user= user_repo.get_user_by_email(db, login_data.email)
    if not user :
        raise ValueError("Invalid Email or Password")
    if not verify_password(login_data.password, user.hashed_password):
        raise ValueError("Invalid Email or Password")
    return user    # Think what did you fetch from DB?

def authenticate_create_token(db:Session, login_data:LoginRequest)->Token:
    user = authenticate_user(db,login_data)
    access_token = create_access_token(user.id,timedelta(minutes=15))
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Now decoding the tokenņ