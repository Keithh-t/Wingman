import os
import jwt
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


JWT_SECRET = os.getenv("JWT_SECRET", "change_this_secret")
JWT_ALG = "HS256"
JWT_TTL_SECONDS = 3600  # 1 hour

def create_token(user_id: int) -> str:
    now = int(time.time())
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + JWT_TTL_SECONDS,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
    return token

def verify_token(token: str) -> int | None:
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        user_id_str = data.get("sub")
        user_id = int(user_id_str) if user_id_str is not None else None
        return user_id
    except Exception:

        return None