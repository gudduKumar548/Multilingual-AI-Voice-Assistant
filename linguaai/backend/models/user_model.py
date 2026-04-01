import hashlib
from sqlalchemy.orm import Session
from models.database import User

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(db: Session, username: str, email: str, password: str) -> bool:
    try:
        user = User(
            username=username.strip(),
            email=email.strip().lower(),
            password_hash=hash_password(password)
        )
        db.add(user)
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def verify_password(db: Session, username: str, password: str) -> bool:
    user = get_user_by_username(db, username)
    if not user:
        return False 
    return user.password_hash == hash_password(password)   
    