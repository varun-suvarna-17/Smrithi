from fastapi import APIRouter, Depends
from app.auth.firebase_middleware import get_current_caregiver_id
from app.models.reminder import ReminderCreate, ReminderStatusUpdate, ReminderOut
from app.services import firestore_service as fs
from app.services.engagement_calc import recompute_engagement


router = APIRouter(
    prefix="/api/patients/{patient_id}/reminders",
    tags=["reminders"]
)


@router.post("", status_code=201)
def create_reminder(
    patient_id: str,
    body: ReminderCreate,
    caregiver_id: str = Depends(get_current_caregiver_id),
):
    """Create a new medicine or activity reminder."""
    reminder_id = fs.create_reminder(
        caregiver_id,
        patient_id,
        body.model_dump()
    )

    return {"reminderId": reminder_id}


@router.get("", status_code=200)
def list_reminders(
    patient_id: str,
    caregiver_id: str = Depends(get_current_caregiver_id),
):
    """List all reminders for a patient."""
    return fs.get_reminders(
        caregiver_id,
        patient_id
    )


@router.patch("/{reminder_id}", status_code=200)
def update_reminder_status(
    patient_id: str,
    reminder_id: str,
    body: ReminderStatusUpdate,
    caregiver_id: str = Depends(get_current_caregiver_id),
):
    """
    Update reminder status (completed / missed / pending).

    Triggers engagement summary recompute so adherence
    rate stays fresh.
    """
    fs.update_reminder(
        caregiver_id,
        patient_id,
        reminder_id,
        body.model_dump()
    )

    summary = recompute_engagement(
        caregiver_id,
        patient_id
    )

    return {
        "status": "updated",
        "engagementSummary": summary.model_dump()
    }