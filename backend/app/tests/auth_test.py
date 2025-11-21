from services.token_utils import create_token, verify_token
from services.auth import hash_password, verify_password

def test_token_round_trip():
    token = create_token(22)
    user_id = verify_token(token)
    assert user_id == 22

def test_verify_token_invalid_returns_none():
    user_id = verify_token("not-a-real-token")
    assert user_id is None

def test_hash_and_verify_password():
    password = "securepassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False