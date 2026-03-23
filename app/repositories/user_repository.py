from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, id: int) -> User | None:
    return db.query(User).filter(User.id == id).first()

def create_user(db: Session, email: str, username: str, hashed_password: str) -> User:
    existing_user = get_user_by_email(db, email)
    
    if existing_user:
        raise ValueError("User already exists")
    
    try:
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    
    except Exception as e:
        db.rollback()
        raise e