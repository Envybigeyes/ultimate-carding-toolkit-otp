import os
from datetime import datetime, timedelta
from jose import jwt

JWT_SECRET = os.getenv("JWT_SECRET")
ALGO = "HS256"

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGO)

def verify_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[ALGO])
