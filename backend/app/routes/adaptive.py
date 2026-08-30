from fastapi import APIRouter, HTTPException, status
from app.database.db import db
from app.schemas import AdaptiveEvaluationRequest, AdaptiveEvaluationResponse, CognitiveGameType
from app.services.adaptive_service import AdaptiveService

router = APIRouter(prefix="/api/adaptive", tags=["Adaptive Difficulty"])

@router.post("/evaluate", response_model=AdaptiveEvaluationResponse)
def evaluate_adaptive_difficulty(req: AdaptiveEvaluationRequest):
    """
    Evaluates patient cognitive metrics using feature extraction and heuristic rules,
    determining whether to increase, maintain, or decrease difficulty level.
    """
    patient = db.patients.find_one({"id": req.patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{req.patient_id}' not found."
        )

    res = AdaptiveService.evaluate_patient_difficulty(
        patient_id=req.patient_id,
        game_type=req.game_type,
        explicit_current_difficulty=req.current_difficulty
    )
    return AdaptiveEvaluationResponse(**res)

@router.get("/patient/{patient_id}/{game_type}", response_model=AdaptiveEvaluationResponse)
def get_patient_game_difficulty(patient_id: str, game_type: CognitiveGameType):
    """Retrieves current adaptive difficulty analysis for patient and game type."""
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )

    res = AdaptiveService.evaluate_patient_difficulty(patient_id=patient_id, game_type=game_type)
    return AdaptiveEvaluationResponse(**res)
