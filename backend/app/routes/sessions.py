from fastapi import APIRouter, Depends
from app.auth.firebase_middleware import get_current_caregiver_id
from app.models.session import SessionCreate, SessionOut
from app.services import firestore_service as fs
from app.services.engagement_calc import recompute_engagement

router = APIRouter(prefix="/api/patients/{patient_id}/sessions", tags=["sessions"])


@router.post("", status_code=201)
def record_session(
    patient_id: str,
    body: SessionCreate,
    caregiver_id: str = Depends(get_current_caregiver_id),
):
    """
    Record a completed or aborted game session.
    Called by the game engine after every session (win or lose).
    Synchronously recomputes engagementSummary/current and returns it so the
    game engine can show an in-game streak toast without a second round trip.
    """
    session_data = body.model_dump()
    # Convert datetime objects to ISO strings for Firestore compatibility
    for field in ("startedAt", "endedAt"):
        if session_data.get(field) is not None:
            session_data[field] = session_data[field]  # kept as datetime — Firestore handles it

    session_id = fs.create_session(caregiver_id, patient_id, session_data)
    summary = recompute_engagement(caregiver_id, patient_id)

    return {
        "sessionId": session_id,
        "engagementSummary": summary.model_dump(),
    }


@router.get("", status_code=200)
def list_sessions(
    patient_id: str,
    caregiver_id: str = Depends(get_current_caregiver_id),
):
    """
    Session history (fallback for non-realtime clients).
    Dashboard frontend should prefer the Firestore onSnapshot listener instead.
    """
    sessions = fs.get_sessions(caregiver_id, patient_id, limit=50)
    return sessions