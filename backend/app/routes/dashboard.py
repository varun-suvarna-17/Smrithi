from fastapi import APIRouter, Depends
from app.auth.firebase_middleware import get_current_caregiver_id
from app.services import firestore_service as fs

router = APIRouter(prefix="/api/patients/{patient_id}/dashboard", tags=["dashboard"])


@router.get("", status_code=200)
def get_dashboard_snapshot(
    patient_id: str,
    caregiver_id: str = Depends(get_current_caregiver_id),
):
    """
    One-shot aggregated snapshot for clients that cannot use Firestore listeners directly.
    Dashboard frontend should prefer onSnapshot listeners on:
      - .../engagementSummary/current
      - .../gameSessions (orderBy startedAt desc, limit 5)
      - .../reminders
    """
    summary = fs.get_engagement_summary(caregiver_id, patient_id) or {}
    recent_sessions = fs.get_sessions(caregiver_id, patient_id, limit=5)
    reminders = fs.get_reminders(caregiver_id, patient_id)

    return {
        "engagementSummary": summary,
        "recentSessions": recent_sessions,
        "reminders": reminders,
    }

