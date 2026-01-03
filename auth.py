# auth.py
import os
from fastapi import Request, HTTPException

def require_internal_auth(request: Request):
    key = request.headers.get("X-Internal-Key")
    if key != os.getenv("INTERNAL_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized")
