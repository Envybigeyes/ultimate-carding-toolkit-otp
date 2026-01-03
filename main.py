from scripts import SCRIPTS
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uuid, random, time, os
import requests

app = FastAPI()

# --- In-memory verification sessions ---
verification_sessions = {}

def create_verification_session(phone, script="capital_one", language="en-US"):
    session_id = str(uuid.uuid4())
    otp = str(random.randint(100000, 999999))

    verification_sessions[session_id] = {
        "phone": phone,
        "otp": otp,
        "attempts": 0,
        "verified": False,
        "script": script,
        "language": language,
        "created_at": time.time()
    }

    return session_id, otp


# --- Send OTP (Vonage SMS placeholder) ---
def send_sms_otp(phone, otp):
    print(f"Sending OTP {otp} to {phone}")
    # TODO: integrate Vonage SMS API


# --- Place Vonage call (Voice API placeholder) ---
def place_call(phone, session_id):
    print(f"Placing call to {phone} with session {session_id}")
    # TODO: integrate Vonage Voice API


# --- Automatic fraud trigger ---
@app.post("/fraud/trigger")
async def fraud_trigger(data: dict):
    phone = data["phone"]
    session_id, otp = create_verification_session(phone)

    send_sms_otp(phone, otp)
    place_call(phone, session_id)

    return {
        "status": "auto_verification_started",
        "session_id": session_id
    }


# --- Manual fraud trigger ---
@app.post("/fraud/manual-call")
async def manual_call(data: dict, request: Request):
    key = request.headers.get("X-Internal-Key")
    if key != os.getenv("INTERNAL_KEY"):
        return {"error": "unauthorized"}

    phone = data["phone"]
    reason = data.get("reason", "manual_fraud_review")
    script = data.get("script", "capital_one")
    language = data.get("language", "en-US")

    session_id, otp = create_verification_session(phone, script, language)

    print(f"Manual fraud call triggered: {reason}")

    send_sms_otp(phone, otp)
    place_call(phone, session_id)

    return {
        "status": "manual_verification_started",
        "session_id": session_id
    }


# --- IVR Answer URL ---
@app.get("/answer")
async def answer(session_id: str):
    # 1️⃣ Load session
    session = verification_sessions.get(session_id)
    if not session:
        return JSONResponse([{
            "action": "talk",
            "text": "We could not locate your verification session. Goodbye."
        }])

    # 2️⃣ Load script + language
    script = SCRIPTS[session["script"]]["languages"][session["language"]]

    # 3️⃣ Build NCCO dynamically
    return JSONResponse([
        {
            "action": "talk",
            "text": script["intro"]
        },
        {
            "action": "talk",
            "text": script["recording"]
        },
        {
            "action": "input",
            "maxDigits": 1,
            "eventUrl": [
                f"https://{os.getenv('FLY_APP_NAME')}.fly.dev/input?session_id={session_id}"
            ]
        }
    ])


# --- IVR input handler ---
@app.post("/input")
async def input(request: Request, session_id: str):
    data = await request.json()
    digit = data.get("dtmf", {}).get("digits")

    # 1️⃣ Load session
    session = verification_sessions.get(session_id)
    if not session:
        return JSONResponse([{
            "action": "talk",
            "text": "Session expired or invalid."
        }])

    # 2️⃣ Load script + language
    script = SCRIPTS[session["script"]]["languages"][session["language"]]

    # 3️⃣ Handle choices
    if digit == "1":
        msg = script["safe"]
    elif digit == "2":
        msg = script["fraud"]
    elif digit == "9":
        msg = script["escalate"]
    else:
        msg = script["retry"]

    return JSONResponse([
        {
            "action": "talk",
            "text": msg
        }
    ])
