import bcrypt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import logging

from database import get_db, User
from database import get_user_by_id  # we’ll define this helper
from services.token_utils import verify_token


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# bcrypt suggested by AI after removing passlib
def hash_password(plain_password: str) -> str:
    """Hash a password using bcrypt."""
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a bcrypt hash."""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_scheme = HTTPBearer(auto_error=False)
COOKIE_NAME = "auth_token"

def require_user(request: Request, creds = Depends(auth_scheme), db: Session = Depends(get_db)) -> User:
    
    token = request.cookies.get(COOKIE_NAME)

    
    if not token and getattr(creds, "credentials", None):
        token = creds.credentials


    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )

    user_id = verify_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    user = get_user_by_id(db, user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )


    return user