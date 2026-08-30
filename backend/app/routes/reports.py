from fastapi import APIRouter, HTTPException, status, Query
from app.database.db import db
from app.schemas import ProgressReportResponse
from app.services.ai_report_service import AIReportService

router = APIRouter(tags=["AI Clinical Progress Reports"])

@router.get("/api/reports/patient/{patient_id}/progress-report", response_model=ProgressReportResponse)
@router.get("/patients/{patient_id}/progress-report", response_model=ProgressReportResponse)
def get_progress_report(patient_id: str, days: int = Query(30, ge=1, le=365)):
    """
    Generates a comprehensive clinical progress summary from actual patient session data.
    Analyzes domain strengths, areas of concern, consistency, and caregiver suggestions.
    Note: Progress-assistance report only; not a medical diagnosis.
    """
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )

    report = AIReportService.generate_progress_report(patient_id=patient_id, days=days)
    return ProgressReportResponse(**report)

@router.post("/api/reports/patient/{patient_id}/generate-summary", response_model=ProgressReportResponse)
def generate_fresh_ai_summary(patient_id: str, days: int = Query(30, ge=1, le=365)):
    """Forces immediate synthesis of a new doctor-ready progress report."""
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )

    report = AIReportService.generate_progress_report(patient_id=patient_id, days=days)
    return ProgressReportResponse(**report)
