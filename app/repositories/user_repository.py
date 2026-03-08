from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, username: str, hashed_password: str) -> User:
    try:
        if get_user_by_email(db,email):
            print("User Alredy exists")
        else:
            user = User(email=email,username=username, hashed_password=hashed_password) # Creating the Object
            db.add(user)  # stage the object -> i want to insert it in db -> added to session's pending changes
            db.commit()  # Actually writes the database -> now SQLAlchemy sends the SQL query to the database 
            db.refresh(user) # Updates the python object -> the database may generate values automatically ( like id and created_at) Relod this object from the databse so it has the latest values
            return user
    except:
        raise 
    