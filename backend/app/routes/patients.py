import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query, Depends
from app.utils.helpers import utc_now_iso
from app.database.db import db
from app.schemas import PatientCreate, PatientUpdate, PatientResponse, ProgressReportResponse
from app.services.ai_report_service import AIReportService

router = APIRouter(prefix="/api/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient_in: PatientCreate):
    """Creates a new elderly dementia patient record."""
    patient_id = f"P{uuid.uuid4().hex[:6].upper()}"

    initial_difficulties = {
        "memory": 1,
        "attention": 1,
        "sequence": 1,
        "pattern": 1,
        "recognition": 1
    }

    patient_doc = {
        "id": patient_id,
        "_id": patient_id,
        "name": patient_in.name,
        "age": patient_in.age,
        "gender": patient_in.gender or "Other",
        "dementia_stage": patient_in.dementia_stage.value,
        "preferred_language": patient_in.preferred_language,
        "emergency_contact": patient_in.emergency_contact,
        "medical_notes": patient_in.medical_notes,
        "baseline_mmse_score": patient_in.baseline_mmse_score,
        "caregiver_id": patient_in.caregiver_id,
        "current_difficulty_levels": initial_difficulties,
        "total_sessions_completed": 0,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso()
    }

    db.patients.insert_one(patient_doc)

    # If linked to a caregiver, add patient to caregiver's assigned list
    if patient_in.caregiver_id:
        cg = db.caregivers.find_one({"id": patient_in.caregiver_id})
        if cg:
            assigned = cg.get("assigned_patients", [])
            if patient_id not in assigned:
                assigned.append(patient_id)
                db.caregivers.update_one({"id": patient_in.caregiver_id}, {"$set": {"assigned_patients": assigned}})

    return PatientResponse(**patient_doc)

@router.get("/", response_model=List[PatientResponse])
def list_patients(
    language: Optional[str] = Query(None, description="Filter by preferred language"),
    caregiver_id: Optional[str] = Query(None, description="Filter by assigned caregiver")
):
    """Lists all registered patients with optional filtering."""
    query = {}
    if language:
        query["preferred_language"] = language
    if caregiver_id:
        query["caregiver_id"] = caregiver_id

    patients = db.patients.find(query=query, sort_by="created_at", reverse=True)
    return [PatientResponse(**p) for p in patients]

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: str):
    """Retrieves patient details by patient ID."""
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )
    return PatientResponse(**patient)

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: str, patient_update: PatientUpdate):
    """Updates an existing patient record."""
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )

    updates = {k: v for k, v in patient_update.model_dump(exclude_unset=True).items() if v is not None}
    if "dementia_stage" in updates and hasattr(updates["dementia_stage"], "value"):
        updates["dementia_stage"] = updates["dementia_stage"].value

    db.patients.update_one({"id": patient_id}, {"$set": updates})
    updated_patient = db.patients.find_one({"id": patient_id})
    return PatientResponse(**updated_patient)

@router.delete("/{patient_id}", status_code=status.HTTP_200_OK)
def delete_patient(patient_id: str):
    """Deletes a patient record."""
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )

    db.patients.delete_one({"id": patient_id})
    return {"success": True, "message": f"Patient '{patient_id}' deleted successfully."}

@router.get("/{patient_id}/progress-report", response_model=ProgressReportResponse)
def get_patient_progress_report(patient_id: str, days: int = Query(30, ge=1, le=365)):
    """Generates structured progress report for patient."""
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )
    report = AIReportService.generate_progress_report(patient_id=patient_id, days=days)
    return ProgressReportResponse(**report)
