import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import profile, sessions, reminders, dashboard, settings, voice

logger = logging.getLogger("smrithi.main")

app = FastAPI(
    title="SPARSH — Smrithi API",
    description=(
        "Backend for SPARSH / Smrithi cognitive-care platform. "
        "All /api/patients/* endpoints require Authorization: Bearer <Firebase ID token>. "
        "Voice TTS endpoints are available under /api/voice/*."
    ),
    version="1.0.0",
)

# ── CORS Middleware ───────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/health", tags=["infra"])
@app.get("/", tags=["infra"])
def health():
    """Liveness check — no auth required."""
    return {
        "status": "ok",
        "app": "SPARSH — Smrithi API",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

# ── PRD Firebase endpoint set ──────────────────────────────────────────────────
app.include_router(profile.router)     # POST/GET/PATCH /api/patients
app.include_router(sessions.router)    # POST/GET /api/patients/{id}/sessions
app.include_router(reminders.router)   # POST/GET/PATCH /api/patients/{id}/reminders
app.include_router(dashboard.router)   # GET /api/patients/{id}/dashboard
app.include_router(settings.router)    # stub (deprecated, kept for import safety)

# ── Voice Layer ───────────────────────────────────────────────────────────────
app.include_router(voice.router)       # POST /api/voice/synthesize, GET /api/voice/stream/{filename}
