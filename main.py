import json
import logging
import os
import time
import urllib.request
from collections import defaultdict, deque
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from knowledge import build_system_instruction

load_dotenv()
logger = logging.getLogger("uvicorn.error")

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

# Comma-separated list, e.g. "https://jeremiah-atoyebi.vercel.app,http://localhost:3000"
ALLOWED_ORIGINS = [
    o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "https://jeremiah-atoyebi.vercel.app,http://localhost:3000").split(",") if o.strip()
]

# Session-summary notifications — optional. If SLACK_WEBHOOK_URL is unset,
# the /session-summary endpoint just no-ops instead of erroring, so the
# feature is safe to leave off in dev. Create one free at
# https://api.slack.com/messaging/webhooks (Slack app → Incoming Webhooks).
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
MAX_SUMMARY_MESSAGES = 200
MAX_SLACK_CHARS = 3500

RATE_LIMIT_MAX = 12
RATE_LIMIT_WINDOW_SECONDS = 60
_request_log: dict[str, deque] = defaultdict(deque)

MAX_HISTORY_TURNS = 12  # caps token usage on long conversations
MAX_MESSAGE_LENGTH = 1000

client = genai.Client(api_key=GEMINI_API_KEY)
SYSTEM_INSTRUCTION = build_system_instruction()

app = FastAPI(title="Portfolio Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class ChatMessage(BaseModel):
    role: str = Field(pattern="^(user|model)$")
    content: str = Field(max_length=MAX_MESSAGE_LENGTH)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)
    history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str


class SessionSummaryRequest(BaseModel):
    messages: list[ChatMessage] = Field(default_factory=list)


def check_rate_limit(client_ip: str) -> None:
    now = time.time()
    log = _request_log[client_ip]
    while log and now - log[0] > RATE_LIMIT_WINDOW_SECONDS:
        log.popleft()
    if len(log) >= RATE_LIMIT_MAX:
        raise HTTPException(status_code=429, detail="Too many messages — please wait a moment and try again.")
    log.append(now)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(client_ip)

    trimmed_history = req.history[-MAX_HISTORY_TURNS:]

    contents = [
        types.Content(role=m.role, parts=[types.Part(text=m.content)]) for m in trimmed_history
    ]
    contents.append(types.Content(role="user", parts=[types.Part(text=req.message)]))

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.6,
                max_output_tokens=800,
            ),
        )
    except Exception as e:
        logger.exception("Gemini generate_content failed")
        raise HTTPException(status_code=502, detail="The chatbot is temporarily unavailable — try again shortly.") from e

    reply = response.text or "Sorry, I didn't catch that — could you rephrase?"
    return ChatResponse(reply=reply)


def _post_session_summary_to_slack(messages: list[ChatMessage]) -> None:
    """Best-effort Slack post of a finished chat session. Never raises —
    this runs as a background task, so failures just get logged."""
    if not SLACK_WEBHOOK_URL:
        return

    lines = []
    for m in messages[:MAX_SUMMARY_MESSAGES]:
        speaker = "Visitor" if m.role == "user" else "Bot"
        lines.append(f"*{speaker}:* {m.content}")
    transcript = "\n".join(lines) if lines else "(no messages)"
    if len(transcript) > MAX_SLACK_CHARS:
        transcript = transcript[:MAX_SLACK_CHARS] + "\n… (truncated)"

    body = json.dumps(
        {"text": f"*Portfolio chatbot — session transcript*\n\n{transcript}"}
    ).encode("utf-8")
    req = urllib.request.Request(
        SLACK_WEBHOOK_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read()
    except Exception as e:
        print(f"[session-summary] failed to post to Slack: {e}")


@app.post("/session-summary")
async def session_summary(request: Request, background_tasks: BackgroundTasks):
    """Called (via navigator.sendBeacon) when a chat session ends, so the
    transcript can be reviewed for upgrade/product purposes. Accepts a raw
    body because sendBeacon can't reliably set a JSON content-type header
    cross-origin without triggering a preflight it doesn't wait for."""
    if not SLACK_WEBHOOK_URL:
        return {"status": "disabled"}

    try:
        raw = await request.body()
        payload = SessionSummaryRequest.model_validate(json.loads(raw))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload")

    if not any(m.role == "user" and m.content.strip() for m in payload.messages):
        return {"status": "skipped"}

    background_tasks.add_task(_post_session_summary_to_slack, payload.messages)
    return {"status": "queued"}