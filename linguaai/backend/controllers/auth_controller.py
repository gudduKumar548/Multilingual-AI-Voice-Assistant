import jwt
import datetime
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config.settings import settings
from models.database import get_db
from models.user_model import create_user, get_user_by_username, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired, please login again")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

def register_user(username: str, email: str, password: str, db: Session):
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    success = create_user(db, username, email, password)
    if not success:
        raise HTTPException(status_code=409, detail="Username or email already exists")
    token = create_token(username)
    return {"access_token": token, "token_type": "bearer", "username": username}

def login_user(username: str, password: str, db: Session):
    if not verify_password(db, username, password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token(username)
    return {"access_token": token, "token_type": "bearer", "username": username}