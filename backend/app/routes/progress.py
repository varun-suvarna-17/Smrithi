from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from app.database.db import db
from app.schemas import PatientAnalyticsResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api", tags=["Cognitive Progress & Analytics"])

@router.get("/progress/{patient_id}")
def get_patient_progress_summary(patient_id: str):
    """Returns concise summary of recent cognitive sessions and domain progression."""
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )

    analytics = AnalyticsService.calculate_patient_analytics(patient_id)
    return {
        "patient_id": patient_id,
        "patient_name": analytics["patient_name"],
        "dementia_stage": analytics["dementia_stage"],
        "total_games_played": analytics["total_games_played"],
        "overall_accuracy_percentage": analytics["overall_accuracy_percentage"],
        "overall_avg_response_time_ms": analytics["overall_avg_response_time_ms"],
        "trajectory": analytics["improvement_indicators"]["overall_trajectory"],
        "consistency_index": analytics["improvement_indicators"]["consistency_index"],
        "recent_sessions": analytics["accuracy_history"][-10:]
    }

@router.get("/analytics/{patient_id}", response_model=PatientAnalyticsResponse)
def get_patient_full_analytics(patient_id: str):
    """
    Returns in-depth cognitive analytics including domain breakdown across all 5 domains,
    historical accuracy trends, latency distributions, and improvement/decline indicators.
    """
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )

    analytics = AnalyticsService.calculate_patient_analytics(patient_id)
    return PatientAnalyticsResponse(**analytics)

@router.get("/analytics/{patient_id}/domain-breakdown")
def get_domain_breakdown(patient_id: str):
    """Retrieves isolated scores and status for each of the 5 cognitive domains."""
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )

    analytics = AnalyticsService.calculate_patient_analytics(patient_id)
    return {
        "patient_id": patient_id,
        "domain_breakdown": analytics["domain_breakdown"],
        "generated_at": analytics["generated_at"]
    }
