from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from jose import jwt
import uuid
import os

from auth import create_token, verify_token
from vonage_client import voice
from models import calls, scripts

BASE_URL = os.getenv("BASE_URL")
FROM_NUMBER = os.getenv("VONAGE_FROM_NUMBER")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- LOGIN ----------------
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin":
        token = create_token(username)
        response = RedirectResponse("/dashboard", status_code=302)
        response.set_cookie("token", token)
        return response
    return RedirectResponse("/", status_code=302)

# ---------------- AUTH DEP ----------------
def require_auth(request: Request):
    token = request.cookies.get("token")
    verify_token(token)
    return True

# ---------------- DASHBOARD ----------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, auth=Depends(require_auth)):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "scripts": scripts}
    )

# ---------------- CALL ----------------
@app.post("/call")
def start_call(
    to: str = Form(...),
    script: str = Form(...),
    record: bool = Form(False),
    auth=Depends(require_auth)
):
    call_id = str(uuid.uuid4())

    response = voice.create_call({
        "to": [{"type": "phone", "number": to}],
        "from": {"type": "phone", "number": FROM_NUMBER},
        "answer_url": [f"{BASE_URL}/answer/{call_id}"],
        "event_url": [f"{BASE_URL}/event/{call_id}"],
        "record": record,
    })

    calls[call_id] = {
        "uuid": response["uuid"],
        "dtmf": [],
        "recording": None
    }

    return RedirectResponse("/dashboard", 302)

# ---------------- ANSWER ----------------
@app.api_route("/answer/{call_id}", methods=["GET", "POST"])
def answer(call_id: str):
    return [
        {"action": "talk", "text": scripts.get("Default")},
        {
            "action": "input",
            "eventUrl": [f"{BASE_URL}/dtmf/{call_id}"],
            "maxDigits": 1
        }
    ]

# ---------------- DTMF ----------------
@app.post("/dtmf/{call_id}")
async def dtmf(call_id: str, request: Request):
    data = await request.json()
    digit = data["dtmf"]["digits"]
    calls[call_id]["dtmf"].append(digit)
    return {"ok": True}

# ---------------- EVENTS ----------------
@app.post("/event/{call_id}")
async def event(call_id: str, request: Request):
    data = await request.json()
    if data["type"] == "recording":
        calls[call_id]["recording"] = data["recording_url"]
    return {"ok": True}
