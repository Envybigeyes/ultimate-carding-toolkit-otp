# auth.py

import os
from fastapi import HTTPException, Request

def require_role(request: Request, role: str):
    token = request.headers.get("X-Auth-Token")

    if role == "admin":
        if token != os.getenv("ADMIN_TOKEN"):
            raise HTTPException(status_code=401, detail="Unauthorized")

    if role == "agent":
        if token not in [os.getenv("ADMIN_TOKEN"), os.getenv("AGENT_TOKEN")]:
            raise HTTPException(status_code=401, detail="Unauthorized")
