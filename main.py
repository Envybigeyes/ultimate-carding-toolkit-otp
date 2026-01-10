import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import vonage
from vonage.auth import Auth

# --------------------
# App setup
# --------------------
app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("JWT_SECRET", "dev-secret")
)

templates = Jinja2Templates(directory="templates")

# --------------------
# Credentials
# --------------------
APP_USERNAME = os.environ.get("APP_USERNAME", "admin")
APP_PASSWORD = os.environ.get("APP_PASSWORD", "admin")

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
VONAGE_NUMBER = os.environ.get("VONAGE_NUMBER")

# --------------------
# Vonage setup
# --------------------
auth = Auth(
    application_id=os.environ["VONAGE_APPLICATION_ID"],
    private_key=os.environ["VONAGE_PRIVATE_KEY"],
)

vonage_client = vonage.Vonage(auth=auth)
voice = vonage_client.voice

# --------------------
# Auth helpers
# --------------------
def require_login(request: Request):
    return request.session.get("user")

# --------------------
# Routes
# --------------------
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if username == APP_USERNAME and password == APP_PASSWORD:
        request.session["user"] = username
        return RedirectResponse("/dashboard", status_code=302)

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid credentials"}
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not require_login(request):
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

@app.post("/call")
async def start_call(
    request: Request,
    to: str = Form(...),
    record: bool = Form(False)
):
    if not require_login(request):
        return RedirectResponse("/", status_code=302)

    voice.create_call({
        "to": [{"type": "phone", "number": to}],
        "from": {"type": "phone", "number": VONAGE_NUMBER},
        "answer_url": [f"{BASE_URL}/answer"],
        "event_url": [f"{BASE_URL}/events"],
        "record": record
    })

    return RedirectResponse("/dashboard", status_code=302)

# --------------------
# Vonage webhooks
# --------------------
@app.post("/answer")
async def answer():
    return JSONResponse([
        {
            "action": "talk",
            "text": "This call may be recorded. Please enter digits now."
        },
        {
            "action": "input",
            "eventUrl": [f"{BASE_URL}/dtmf"],
            "maxDigits": 10,
            "submitOnHash": True
        }
    ])

@app.post("/dtmf")
async def dtmf(event: dict):
    digits = event.get("dtmf", {}).get("digits")
    print("DTMF received:", digits)
    return {"status": "ok"}

@app.post("/events")
async def events(event: dict):
    print("CALL EVENT:", event)
    return {"status": "ok"}
