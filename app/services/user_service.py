from app.schemas.user_schemas import CreateUser, UserResponse
from sqlalchemy.orm import Session
'''why this architecture for tje real production system'''
'''
What the service should receive 
-> db: Session - so it can call the repository, need to interact with repo
-> user_data: CreateUser - schema from the API layer, comes from API validation layer
What the service should return 
-> UserResponse (or UserRead) - a response schema, not ORM
'''
def register_user(db: Session, user_data: CreateUser) -> UserResponse:
    pass 
