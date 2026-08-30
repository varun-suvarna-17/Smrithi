import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from app.utils.helpers import utc_now_iso
from app.database.db import db
from app.schemas import (
    CaregiverCreate, CaregiverUpdate, CaregiverResponse,
    CaregiverPatientLink, PatientResponse, AlertItem
)

router = APIRouter(prefix="/api/caregivers", tags=["Caregivers"])

@router.post("/", response_model=CaregiverResponse, status_code=status.HTTP_201_CREATED)
def create_caregiver(caregiver_in: CaregiverCreate):
    """Registers a new caregiver profile."""
    caregiver_id = f"cg_{uuid.uuid4().hex[:8]}"

    caregiver_doc = {
        "id": caregiver_id,
        "_id": caregiver_id,
        "name": caregiver_in.name,
        "relationship": caregiver_in.relationship,
        "phone": caregiver_in.phone,
        "email": caregiver_in.email,
        "user_id": caregiver_in.user_id,
        "assigned_patients": [],
        "created_at": utc_now_iso()
    }

    db.caregivers.insert_one(caregiver_doc)
    return CaregiverResponse(**caregiver_doc)

@router.get("/", response_model=List[CaregiverResponse])
def list_caregivers():
    """Lists all registered caregivers."""
    caregivers = db.caregivers.find(sort_by="created_at", reverse=True)
    return [CaregiverResponse(**cg) for cg in caregivers]

@router.get("/{caregiver_id}", response_model=CaregiverResponse)
def get_caregiver(caregiver_id: str):
    """Retrieves caregiver profile by ID."""
    cg = db.caregivers.find_one({"id": caregiver_id})
    if not cg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caregiver with ID '{caregiver_id}' not found."
        )
    return CaregiverResponse(**cg)

@router.put("/{caregiver_id}", response_model=CaregiverResponse)
def update_caregiver(caregiver_id: str, updates_in: CaregiverUpdate):
    """Updates caregiver details."""
    cg = db.caregivers.find_one({"id": caregiver_id})
    if not cg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caregiver with ID '{caregiver_id}' not found."
        )

    updates = {k: v for k, v in updates_in.model_dump(exclude_unset=True).items() if v is not None}
    db.caregivers.update_one({"id": caregiver_id}, {"$set": updates})
    updated = db.caregivers.find_one({"id": caregiver_id})
    return CaregiverResponse(**updated)

@router.post("/associate", status_code=status.HTTP_200_OK)
def associate_patient_caregiver(link: CaregiverPatientLink):
    """Associates a patient with a designated caregiver."""
    patient = db.patients.find_one({"id": link.patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{link.patient_id}' not found."
        )

    caregiver = db.caregivers.find_one({"id": link.caregiver_id})
    if not caregiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caregiver with ID '{link.caregiver_id}' not found."
        )

    # Update patient
    db.patients.update_one({"id": link.patient_id}, {"$set": {"caregiver_id": link.caregiver_id}})

    # Update caregiver assigned list
    assigned = caregiver.get("assigned_patients", [])
    if link.patient_id not in assigned:
        assigned.append(link.patient_id)
        db.caregivers.update_one({"id": link.caregiver_id}, {"$set": {"assigned_patients": assigned}})

    return {
        "success": True,
        "message": f"Successfully associated patient '{patient.get('name')}' with caregiver '{caregiver.get('name')}'."
    }

@router.post("/disassociate", status_code=status.HTTP_200_OK)
def disassociate_patient_caregiver(link: CaregiverPatientLink):
    """Removes association between a patient and caregiver."""
    patient = db.patients.find_one({"id": link.patient_id})
    caregiver = db.caregivers.find_one({"id": link.caregiver_id})

    if patient and patient.get("caregiver_id") == link.caregiver_id:
        db.patients.update_one({"id": link.patient_id}, {"$set": {"caregiver_id": None}})

    if caregiver:
        assigned = [p for p in caregiver.get("assigned_patients", []) if p != link.patient_id]
        db.caregivers.update_one({"id": link.caregiver_id}, {"$set": {"assigned_patients": assigned}})

    return {"success": True, "message": "Disassociation completed."}

@router.get("/{caregiver_id}/patients", response_model=List[PatientResponse])
def list_assigned_patients(caregiver_id: str):
    """Lists all patients assigned to this caregiver."""
    caregiver = db.caregivers.find_one({"id": caregiver_id})
    if not caregiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caregiver with ID '{caregiver_id}' not found."
        )

    assigned_ids = caregiver.get("assigned_patients", [])
    patients = [db.patients.find_one({"id": pid}) for pid in assigned_ids]
    patients = [p for p in patients if p is not None]
    return [PatientResponse(**p) for p in patients]

@router.get("/{caregiver_id}/alerts", response_model=List[AlertItem])
def get_caregiver_alerts(caregiver_id: str):
    """Retrieves urgent alerts and notifications for the caregiver."""
    caregiver = db.caregivers.find_one({"id": caregiver_id})
    if not caregiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caregiver with ID '{caregiver_id}' not found."
        )

    assigned_ids = caregiver.get("assigned_patients", [])
    all_alerts = db.alerts.find(sort_by="created_at", reverse=True)
    caregiver_alerts = [
        a for a in all_alerts
        if a.get("caregiver_id") == caregiver_id or a.get("patient_id") in assigned_ids
    ]
    return [AlertItem(**a) for a in caregiver_alerts]

@router.patch("/alerts/{alert_id}/read")
def mark_alert_read(alert_id: str):
    """Marks a caregiver alert as acknowledged/read."""
    alert = db.alerts.find_one({"id": alert_id})
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with ID '{alert_id}' not found."
        )
    db.alerts.update_one({"id": alert_id}, {"$set": {"is_read": True}})
    return {"success": True, "alert_id": alert_id, "is_read": True}
