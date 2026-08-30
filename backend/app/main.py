import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.database.db import db
from app.middleware.error_handler import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler
)
from app.routes import (
    auth,
    patients,
    caregivers,
    games,
    adaptive,
    progress,
    languages,
    voice,
    reminders,
    reports
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("smrithi.main")

def seed_initial_demo_data():
    """Seeds realistic demo patient, caregiver, and baseline session data for instant Postman testing."""
    if db.patients.count() == 0:
        # Seed Caregiver
        cg_id = "cg_demo_001"
        db.caregivers.insert_one({
            "id": cg_id,
            "_id": cg_id,
            "name": "Ananya Sharma",
            "relationship": "Daughter & Primary Caregiver",
            "phone": "+91-9876543210",
            "email": "ananya.caregiver@smrithi.org",
            "assigned_patients": ["P001"],
            "created_at": "2026-08-01T08:00:00"
        })

        # Seed Patient P001 (Biren Borthakur, 74, Assamese)
        db.patients.insert_one({
            "id": "P001",
            "_id": "P001",
            "name": "Biren Borthakur",
            "age": 74,
            "gender": "Male",
            "dementia_stage": "Early Stage",
            "preferred_language": "as",
            "emergency_contact": "+91-9876543210 (Ananya Sharma)",
            "medical_notes": "Mild short-term memory deficit. Highly responsive to Assamese cultural symbols and folk music cues.",
            "baseline_mmse_score": 24,
            "caregiver_id": cg_id,
            "current_difficulty_levels": {
                "memory": 2,
                "attention": 2,
                "sequence": 1,
                "pattern": 2,
                "recognition": 2
            },
            "total_sessions_completed": 8,
            "created_at": "2026-08-01T08:30:00",
            "updated_at": "2026-08-29T10:00:00"
        })

        # Seed initial session attempts for P001 to demonstrate analytics & AI reports
        sample_attempts = [
            {
                "id": "att_demo_01",
                "patient_id": "P001",
                "session_id": "sess_demo_01",
                "game_type": "memory",
                "cognitive_domain": "Memory",
                "difficulty_level": 1,
                "score": 3,
                "total_questions": 3,
                "correct_answers": 3,
                "accuracy": 100.0,
                "response_time_ms": 3200,
                "mistakes": 0,
                "attempts": 1,
                "session_duration_seconds": 45,
                "timestamp": "2026-08-20T09:00:00"
            },
            {
                "id": "att_demo_02",
                "patient_id": "P001",
                "session_id": "sess_demo_02",
                "game_type": "attention",
                "cognitive_domain": "Attention",
                "difficulty_level": 1,
                "score": 3,
                "total_questions": 3,
                "correct_answers": 3,
                "accuracy": 100.0,
                "response_time_ms": 4100,
                "mistakes": 0,
                "attempts": 1,
                "session_duration_seconds": 60,
                "timestamp": "2026-08-22T09:30:00"
            },
            {
                "id": "att_demo_03",
                "patient_id": "P001",
                "session_id": "sess_demo_03",
                "game_type": "sequence",
                "cognitive_domain": "Reasoning & Sequence",
                "difficulty_level": 1,
                "score": 2,
                "total_questions": 3,
                "correct_answers": 2,
                "accuracy": 66.7,
                "response_time_ms": 5800,
                "mistakes": 1,
                "attempts": 2,
                "session_duration_seconds": 80,
                "timestamp": "2026-08-24T10:00:00"
            },
            {
                "id": "att_demo_04",
                "patient_id": "P001",
                "session_id": "sess_demo_04",
                "game_type": "memory",
                "cognitive_domain": "Memory",
                "difficulty_level": 2,
                "score": 4,
                "total_questions": 4,
                "correct_answers": 4,
                "accuracy": 100.0,
                "response_time_ms": 3400,
                "mistakes": 0,
                "attempts": 1,
                "session_duration_seconds": 55,
                "timestamp": "2026-08-26T09:15:00"
            },
            {
                "id": "att_demo_05",
                "patient_id": "P001",
                "session_id": "sess_demo_05",
                "game_type": "pattern",
                "cognitive_domain": "Pattern Recognition",
                "difficulty_level": 2,
                "score": 3,
                "total_questions": 4,
                "correct_answers": 3,
                "accuracy": 75.0,
                "response_time_ms": 4600,
                "mistakes": 1,
                "attempts": 1,
                "session_duration_seconds": 70,
                "timestamp": "2026-08-28T09:45:00"
            }
        ]
        for att in sample_attempts:
            db.game_attempts.insert_one(att)

        # Seed sample reminder
        db.reminders.insert_one({
            "id": "rem_demo_01",
            "patient_id": "P001",
            "title": "Morning Memory Exercise",
            "message": "Complete today's 10-minute North Eastern Memory Activity on Smrithi.",
            "reminder_type": "cognitive_game",
            "scheduled_time": "2026-08-29T10:00:00",
            "recurring": True,
            "frequency": "daily",
            "is_completed": False,
            "caregiver_id": cg_id,
            "created_at": "2026-08-01T08:00:00"
        })
        logger.info("Demo patient 'P001' and sample cognitive sessions seeded successfully.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing SMRITHI REST Backend...")
    db.connect()
    seed_initial_demo_data()
    yield
    # Shutdown
    logger.info("SMRITHI Backend shutting down.")

app = FastAPI(
    title="SMRITHI Backend REST API",
    description="""
# SMRITHI – AI-Based Cognitive Gaming and Memory Assistance Platform for Elderly Dementia Patients in the North Eastern Region (NER)
### Problem Statement: SIH26003

This is a **REST API Backend** built for elderly dementia care in North East India.
It provides:
* **Elderly Patient & Caregiver Management**: Profile lifecycle, emergency contacts, dementia stages, and role associations.
* **5 Culturally-Themed Cognitive Games**: Memory Match, Focused Attention, Routine Sequence Recall, Folk Motif Patterns, and Heritage Recognition.
* **Multi-Factor Adaptive Difficulty Engine**: Feature extraction pipeline (accuracy, response latency, streak, trend slope) and explainable heuristic & ML interfaces.
* **Cognitive Domain Analytics**: Trajectory tracking, consistency index, response latency analysis, and domain scoring.
* **Multilingual NER Support**: Localization dictionary and translation hooks for Assamese, Bengali, Manipuri, Bodo, Mizo, Khasi, Garo, Hindi, and English.
* **Voice & Text-To-Speech (TTS)**: Speech synthesis service for cognitive instructions.
* **Reminders & Alert Notifications**: Scheduled daily routine reminders and performance-drop alert triggers.
* **AI & Clinical Progress Summaries**: Data-driven progress reports with Gemini / clinical rule-based generation and doctor-ready summaries.
* **Role-Based JWT Authentication**: Secure password hashing with bcrypt and token protection.

*Disclaimer: Progress-assistance reports generated by SMRITHI are designed for caregiver and clinician monitoring, NOT as diagnostic replacements for clinical neuropsychological assessment.*
    """,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Global Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include Routers
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(caregivers.router)
app.include_router(games.router)
app.include_router(adaptive.router)
app.include_router(progress.router)
app.include_router(languages.router)
app.include_router(voice.router)
app.include_router(reminders.router)
app.include_router(reports.router)

@app.get("/", tags=["Health"])
@app.get("/health", tags=["Health"])
def health_check():
    """Health check and backend system overview."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database_mode": db.mode,
        "database_connected": db.is_connected,
        "total_patients": db.patients.count(),
        "total_games_supported": 5,
        "supported_languages_count": 9,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "message": "SMRITHI Backend API is running successfully."
    }
