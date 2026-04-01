from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from controllers.auth_controller import register_user, login_user, get_current_user
from models.database import get_db

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(req.username, req.email, req.password, db)

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_user(form.username, form.password, db)

@router.get("/me")
def me(username: str = Depends(get_current_user)):
    return {"username": username}