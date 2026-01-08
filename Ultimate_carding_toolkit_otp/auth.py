# auth.py
import os
from fastapi import Request, HTTPException

def require_role(request: Request, role: str):
    """
    Roles:
    - admin → X-Auth-Token header
    - agent → session cookie
    """

    if role == "admin":
        token = request.headers.get("X-Auth-Token")
        if token != os.getenv("ADMIN_TOKEN"):
            raise HTTPException(status_code=401, detail="Admin unauthorized")

    elif role == "agent":
        token = request.cookies.get("session")
        if token not in [os.getenv("ADMIN_TOKEN"), os.getenv("AGENT_TOKEN")]:
            raise HTTPException(status_code=401, detail="Agent unauthorized")

    else:
        raise HTTPException(status_code=403, detail="Invalid role")
