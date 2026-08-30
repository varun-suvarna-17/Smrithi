import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query
from app.utils.helpers import utc_now_iso
from app.database.db import db
from app.schemas import (
    GameInfo, StartGameRequest, StartGameResponse,
    GameAttemptCreate, GameAttemptResponse, CognitiveGameType,
    AdaptiveEvaluationResponse
)
from app.services.game_service import GameService, GAMES_REGISTRY
from app.services.adaptive_service import AdaptiveService

router = APIRouter(prefix="/api/games", tags=["Cognitive Games"])

@router.get("/", response_model=List[GameInfo])
def list_games():
    """Lists all 5 available cognitive games with cultural North Eastern context and domains."""
    return GameService.list_games()

@router.get("/{game_type}", response_model=GameInfo)
def get_game_details(game_type: CognitiveGameType):
    """Retrieves specific cognitive game metadata."""
    info = GameService.get_game_info(game_type)
    if not info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game type '{game_type}' not found."
        )
    return info

@router.post("/start", response_model=StartGameResponse)
def start_game_session(req: StartGameRequest):
    """
    Initializes a new game session and returns tailored interactive round questions
    based on the patient's current adaptive level and preferred language.
    """
    patient = db.patients.find_one({"id": req.patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{req.patient_id}' not found."
        )

    # Determine difficulty level
    difficulty = req.difficulty_level
    if difficulty is None:
        diff_levels = patient.get("current_difficulty_levels", {})
        difficulty = diff_levels.get(req.game_type.value, 1)

    # Determine language
    language = req.language or patient.get("preferred_language", "as")

    # Generate game data
    session_data = GameService.generate_game_session(
        patient_id=req.patient_id,
        game_type=req.game_type,
        difficulty_level=difficulty,
        language=language
    )

    return StartGameResponse(**session_data)

@router.post("/submit-result", response_model=GameAttemptResponse, status_code=status.HTTP_201_CREATED)
def submit_game_result(attempt_in: GameAttemptCreate):
    """
    Submits a completed game attempt, stores performance metrics,
    evaluates adaptive difficulty, and returns updated progression recommendations.
    """
    patient = db.patients.find_one({"id": attempt_in.patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{attempt_in.patient_id}' not found."
        )

    attempt_id = f"att_{uuid.uuid4().hex[:10]}"
    accuracy = round((attempt_in.correct_answers / max(1, attempt_in.total_questions)) * 100.0, 1)
    game_info = GameService.get_game_info(attempt_in.game_type)
    domain_name = game_info.cognitive_domain.value if game_info else "Cognitive Domain"

    attempt_doc = {
        "id": attempt_id,
        "_id": attempt_id,
        "patient_id": attempt_in.patient_id,
        "session_id": attempt_in.session_id,
        "game_type": attempt_in.game_type.value,
        "cognitive_domain": domain_name,
        "difficulty_level": attempt_in.difficulty_level,
        "score": attempt_in.score,
        "total_questions": attempt_in.total_questions,
        "correct_answers": attempt_in.correct_answers,
        "accuracy": accuracy,
        "response_time_ms": attempt_in.response_time_ms,
        "mistakes": attempt_in.mistakes,
        "attempts": attempt_in.attempts,
        "session_duration_seconds": attempt_in.session_duration_seconds or 60,
        "details": attempt_in.details or [],
        "timestamp": utc_now_iso()
    }

    db.game_attempts.insert_one(attempt_doc)

    # Increment patient's total session count
    current_count = patient.get("total_sessions_completed", 0) + 1
    db.patients.update_one({"id": attempt_in.patient_id}, {"$set": {"total_sessions_completed": current_count}})

    # Trigger Adaptive Difficulty evaluation
    adaptive_result = AdaptiveService.evaluate_patient_difficulty(
        patient_id=attempt_in.patient_id,
        game_type=attempt_in.game_type,
        explicit_current_difficulty=attempt_in.difficulty_level
    )

    return GameAttemptResponse(
        id=attempt_id,
        patient_id=attempt_in.patient_id,
        session_id=attempt_in.session_id,
        game_type=attempt_in.game_type.value,
        cognitive_domain=domain_name,
        difficulty_level=attempt_in.difficulty_level,
        score=attempt_in.score,
        total_questions=attempt_in.total_questions,
        correct_answers=attempt_in.correct_answers,
        accuracy=accuracy,
        response_time_ms=attempt_in.response_time_ms,
        mistakes=attempt_in.mistakes,
        attempts=attempt_in.attempts,
        session_duration_seconds=attempt_doc["session_duration_seconds"],
        timestamp=attempt_doc["timestamp"],
        next_recommended_difficulty=adaptive_result["recommended_difficulty"],
        adaptive_recommendation=adaptive_result["rationale"]
    )

@router.get("/attempts/{patient_id}", response_model=List[GameAttemptResponse])
def get_patient_game_history(
    patient_id: str,
    game_type: Optional[CognitiveGameType] = Query(None, description="Filter by game type"),
    limit: int = Query(50, ge=1, le=200)
):
    """Retrieves chronological game history and performance records for a patient."""
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )

    query = {"patient_id": patient_id}
    if game_type:
        query["game_type"] = game_type.value

    attempts = db.game_attempts.find(query=query, sort_by="timestamp", reverse=True, limit=limit)
    
    results = []
    for a in attempts:
        results.append(GameAttemptResponse(
            id=a.get("id", str(a.get("_id"))),
            patient_id=a.get("patient_id"),
            session_id=a.get("session_id"),
            game_type=a.get("game_type"),
            cognitive_domain=a.get("cognitive_domain", "Cognitive Domain"),
            difficulty_level=a.get("difficulty_level", 1),
            score=a.get("score", 0),
            total_questions=a.get("total_questions", 1),
            correct_answers=a.get("correct_answers", 0),
            accuracy=a.get("accuracy", 0.0),
            response_time_ms=a.get("response_time_ms", 0),
            mistakes=a.get("mistakes", 0),
            attempts=a.get("attempts", 1),
            session_duration_seconds=a.get("session_duration_seconds", 0),
            timestamp=a.get("timestamp", utc_now_iso()),
            next_recommended_difficulty=a.get("difficulty_level", 1),
            adaptive_recommendation="Archived Attempt"
        ))
    return results

@router.get("/adaptive-difficulty/{patient_id}/{game_type}", response_model=AdaptiveEvaluationResponse)
def get_adaptive_difficulty(patient_id: str, game_type: CognitiveGameType):
    """Evaluates and returns next recommended difficulty and clinical rationale."""
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )

    res = AdaptiveService.evaluate_patient_difficulty(patient_id=patient_id, game_type=game_type)
    return AdaptiveEvaluationResponse(**res)
