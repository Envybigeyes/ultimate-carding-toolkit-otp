# auth.py
import os
from fastapi import Request, HTTPException

def require_role(request, role):
    token = request.headers.get("X-Auth-Token")
    if role == "admin" and token != os.getenv("ADMIN_TOKEN"):
        raise HTTPException(status_code=401)
    if role == "agent" and token not in [os.getenv("ADMIN_TOKEN"), os.getenv("AGENT_TOKEN")]:
        raise HTTPException(status_code=401)
