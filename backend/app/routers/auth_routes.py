from fastapi import APIRouter, FastAPI, Depends, HTTPException, status, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import logging

from database import get_db, get_user_by_email, create_user, User
from services.auth import hash_password, verify_password, require_user
from services.token_utils import create_token

router = APIRouter(prefix="/api", tags=["auth"])
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

COOKIE_NAME = "auth_token"
COOKIE_MAX_AGE =  60 * 60 * 2  # 2 hours

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
def register_user(payload: RegisterRequest, db: Session = Depends(get_db), response: Response = None):
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
    response.set_cookie(key=COOKIE_NAME,
                        value=token, 
                        httponly=True,
                        # secure=True,
                        samesite="lax",
                        max_age=COOKIE_MAX_AGE,
                        path="/")
    
    return AuthResponse(token="(cookie)", user_id=user.id, username=user.username, email=user.email)

@router.post("/login", response_model=AuthResponse)
def login_user(payload: LoginRequest, db: Session = Depends(get_db), response: Response = None):
    user = get_user_by_email(db, payload.email)
    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = create_token(user.id)
    response.set_cookie(key=COOKIE_NAME,
                        value=token, 
                        httponly=True,
                        # secure=True,
                        samesite="lax",
                        max_age=COOKIE_MAX_AGE,
                        path="/")

    return AuthResponse(token="(cookie)", user_id=user.id, username=user.username, email=user.email)

@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie(key=COOKIE_NAME)
    return {"detail": "Logged out successfully"}

@router.get("/me", response_model=UserInfoResponse)
def get_current_user(current_user: User = Depends(require_user)):
    return UserInfoResponse(user_id=current_user.id, username=current_user.username, email=current_user.email)