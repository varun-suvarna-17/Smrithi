from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.firebase_middleware import get_current_caregiver_id
from app.models.patient import PatientCreate, PatientUpdate, PatientOut
from app.services import firestore_service as fs

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.post("", status_code=201)
def create_patient(
    body: PatientCreate,
    caregiver_id: str = Depends(get_current_caregiver_id),
):
    """Create a patient profile under the authenticated caregiver."""
    patient_id = fs.create_patient(caregiver_id, body.model_dump())
    return {"patientId": patient_id}


@router.get("/{patient_id}")
def get_patient(
    patient_id: str,
    caregiver_id: str = Depends(get_current_caregiver_id),
):
    """Fetch a patient profile. Also used by game engine at session start to read difficultyLevel."""
    return fs.get_patient(caregiver_id, patient_id)


@router.patch("/{patient_id}", status_code=200)
def update_patient(
    patient_id: str,
    body: PatientUpdate,
    caregiver_id: str = Depends(get_current_caregiver_id),
):
    """Update mutable patient fields (e.g. contentLanguage, avatarAssetId)."""
    data = {k: v for k, v in body.model_dump().items() if v is not None}
    if not data:
        raise HTTPException(status_code=400, detail="No fields provided to update.")
    fs.update_patient(caregiver_id, patient_id, data)
    return {"status": "updated"}