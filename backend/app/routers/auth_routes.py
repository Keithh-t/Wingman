from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from database import get_db, get_user_by_email, create_user, User
from services.auth import hash_password, verify_password, require_user
from services.token_utils import create_token

router = APIRouter(prefix="/api", tags=["auth"])

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    token: str
    user_id: int
    username: str
    email: EmailStr

class UserInfoResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr

@router.post("/register", response_model=AuthResponse)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    password_hash = hash_password(payload.password)
    user = create_user(
        db,
        username=payload.username,
        email=payload.email,
        password_hash=password_hash,
        google_id=None,
    )
    token = create_token(user.id)
    return AuthResponse(token=token, user_id=user.id, username=user.username, email=user.email)

@router.post("/login", response_model=AuthResponse)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = create_token(user.id)
    return AuthResponse(token=token, user_id=user.id, username=user.username, email=user.email)

@router.get("/me", response_model=UserInfoResponse)
def get_current_user(current_user: User = Depends(require_user)):
    return UserInfoResponse(user_id=current_user.id, username=current_user.username, email=current_user.email)