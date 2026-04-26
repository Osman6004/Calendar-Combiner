from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
import httpx
import os
from datetime import datetime, timezone
from typing import Optional
import json
import secrets
import time

app = FastAPI(title="Calendar Combiner")

GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (use Redis in production)
sessions: dict[str, dict] = {}

SCOPES = "https://www.googleapis.com/auth/calendar.freebusy https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/auth/login")
def login(session_id: str, participant_index: int = 0):
    state = json.dumps({"session_id": session_id, "participant_index": participant_index})
    import base64
    state_b64 = base64.urlsafe_b64encode(state.encode()).decode()

    redirect_uri = f"{BACKEND_URL}/auth/callback"
    url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope={SCOPES}"
        f"&state={state_b64}"
        f"&access_type=offline"
        f"&prompt=select_account"
    )
    return RedirectResponse(url)


@app.get("/auth/callback")
async def callback(code: str, state: str):
    import base64
    try:
        state_data = json.loads(base64.urlsafe_b64decode(state + "==").decode())
        session_id = state_data["session_id"]
        participant_index = state_data["participant_index"]
    except Exception:
        raise HTTPException(400, "Invalid state")

    redirect_uri = f"{BACKEND_URL}/auth/callback"
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        tokens = token_resp.json()
        if "error" in tokens:
            raise HTTPException(400, tokens["error"])

        access_token = tokens["access_token"]

        user_resp = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info = user_resp.json()

    if session_id not in sessions:
        sessions[session_id] = {"participants": {}}

    sessions[session_id]["participants"][str(participant_index)] = {
        "access_token": access_token,
        "name": user_info.get("given_name") or user_info.get("name", f"Person {participant_index + 1}"),
        "email": user_info.get("email", ""),
        "picture": user_info.get("picture", ""),
        "connected_at": time.time(),
    }

    return HTMLResponse(f"""
        <html><head><title>Connected!</title></head>
        <body style="font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;background:#f9f9f9;">
        <div style="text-align:center;padding:2rem;background:white;border-radius:12px;border:1px solid #e0e0e0;">
            <div style="font-size:32px;margin-bottom:12px;">✓</div>
            <h2 style="margin:0 0 8px;font-weight:500;">Connected!</h2>
            <p style="color:#666;margin:0 0 16px;">Signed in as <strong>{user_info.get('email','')}</strong></p>
            <p style="color:#999;font-size:13px;">You can close this tab and return to Calendar Combiner.</p>
        </div>
        <script>
            setTimeout(() => window.close(), 2000);
        </script>
        </body></html>
    """)


@app.get("/session/{session_id}")
def get_session(session_id: str):
    session = sessions.get(session_id, {"participants": {}})
    safe = {}
    for idx, p in session.get("participants", {}).items():
        safe[idx] = {"name": p["name"], "email": p["email"], "picture": p["picture"]}
    return {"participants": safe}


class FreeBusyRequest(BaseModel):
    session_id: str
    date_from: str
    date_to: str
    time_from: str = "09:00"
    time_to: str = "17:00"
    min_duration_minutes: int = 30


@app.post("/find-overlaps")
async def find_overlaps(req: FreeBusyRequest):
    session = sessions.get(req.session_id)
    if not session or len(session.get("participants", {})) < 2:
        raise HTTPException(400, "Need at least 2 connected participants")

    time_min = f"{req.date_from}T00:00:00Z"
    time_max = f"{req.date_to}T23:59:59Z"

    all_busy: list[tuple[datetime, datetime]] = []

    async with httpx.AsyncClient() as client:
        for idx, p in session["participants"].items():
            resp = await client.post(
                "https://www.googleapis.com/calendar/v3/freeBusy",
                headers={"Authorization": f"Bearer {p['access_token']}"},
                json={
                    "timeMin": time_min,
                    "timeMax": time_max,
                    "items": [{"id": "primary"}],
                },
            )
            data = resp.json()
            busy_periods = data.get("calendars", {}).get("primary", {}).get("busy", [])
            for b in busy_periods:
                start = datetime.fromisoformat(b["start"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(b["end"].replace("Z", "+00:00"))
                all_busy.append((start, end))

    slots = generate_slots(req.date_from, req.date_to, req.time_from, req.time_to, req.min_duration_minutes)
    free_slots = [s for s in slots if not overlaps_any(s, all_busy)]

    return {
        "slots": [
            {
                "start": s[0].isoformat(),
                "end": s[1].isoformat(),
                "duration_minutes": req.min_duration_minutes,
            }
            for s in free_slots
        ],
        "total": len(free_slots),
    }


def generate_slots(date_from, date_to, time_from, time_to, duration_min):
    from datetime import timedelta, date
    slots = []
    fh, fm = map(int, time_from.split(":"))
    th, tm = map(int, time_to.split(":"))
    cur = date.fromisoformat(date_from)
    end = date.fromisoformat(date_to)
    delta = timedelta(minutes=duration_min)

    while cur <= end:
        if cur.weekday() < 5:  # Mon-Fri
            slot_start = datetime(cur.year, cur.month, cur.day, fh, fm, tzinfo=timezone.utc)
            day_end = datetime(cur.year, cur.month, cur.day, th, tm, tzinfo=timezone.utc)
            while slot_start + delta <= day_end:
                slots.append((slot_start, slot_start + delta))
                slot_start += delta
        from datetime import timedelta as td
        cur = cur + td(days=1)
    return slots


def overlaps_any(slot, busy_list):
    s_start, s_end = slot
    for b_start, b_end in busy_list:
        if s_start < b_end and s_end > b_start:
            return True
    return False
