from app.core.firebase_init import db
from datetime import datetime, timezone
from fastapi import HTTPException, status
from google.cloud.firestore_v1 import SERVER_TIMESTAMP


def _get_db():
    if db is None:
        raise RuntimeError(
            "Firestore client is not initialized. "
            "Ensure serviceAccountKey.json is present or Firebase env vars are set."
        )
    return db


def _caregiver_ref(caregiver_id: str):
    return _get_db().collection("caregivers").document(caregiver_id)


def _patient_ref(caregiver_id: str, patient_id: str):
    return _caregiver_ref(caregiver_id).collection("patients").document(patient_id)


def _assert_patient_owned(caregiver_id: str, patient_id: str):
    """Raises HTTP 403 if the patient doc doesn't exist under this caregiver."""
    doc = _patient_ref(caregiver_id, patient_id).get()
    if not doc.exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient not found or not owned by this caregiver.",
        )
    return doc


# ── Caregiver ────────────────────────────────────────────────────────────────

def upsert_caregiver(caregiver_id: str, data: dict):
    """Creates or updates the top-level caregiver document."""
    data["updatedAt"] = SERVER_TIMESTAMP
    _caregiver_ref(caregiver_id).set(data, merge=True)


# ── Patients ─────────────────────────────────────────────────────────────────

def create_patient(caregiver_id: str, data: dict) -> str:
    data["createdAt"] = SERVER_TIMESTAMP
    doc_ref = _caregiver_ref(caregiver_id).collection("patients").document()
    doc_ref.set(data)
    return doc_ref.id


def get_patient(caregiver_id: str, patient_id: str) -> dict:
    doc = _assert_patient_owned(caregiver_id, patient_id)
    result = doc.to_dict()
    result["patientId"] = doc.id
    return result


def update_patient(caregiver_id: str, patient_id: str, data: dict):
    _assert_patient_owned(caregiver_id, patient_id)
    data["updatedAt"] = SERVER_TIMESTAMP
    _patient_ref(caregiver_id, patient_id).update(data)


# ── Game Sessions ─────────────────────────────────────────────────────────────

def create_session(caregiver_id: str, patient_id: str, data: dict) -> str:
    _assert_patient_owned(caregiver_id, patient_id)
    data["createdAt"] = SERVER_TIMESTAMP
    doc_ref = (
        _patient_ref(caregiver_id, patient_id)
        .collection("gameSessions")
        .document()
    )
    doc_ref.set(data)
    return doc_ref.id


def get_sessions(caregiver_id: str, patient_id: str, limit: int = 50) -> list:
    _assert_patient_owned(caregiver_id, patient_id)
    docs = (
        _patient_ref(caregiver_id, patient_id)
        .collection("gameSessions")
        .order_by("startedAt", direction="DESCENDING")
        .limit(limit)
        .stream()
    )
    return [{**doc.to_dict(), "sessionId": doc.id} for doc in docs]


def get_all_sessions_since(caregiver_id: str, patient_id: str, since: datetime) -> list:
    """Returns all sessions with startedAt >= since (for streak / weekly calc)."""
    docs = (
        _patient_ref(caregiver_id, patient_id)
        .collection("gameSessions")
        .where("startedAt", ">=", since)
        .order_by("startedAt", direction="DESCENDING")
        .stream()
    )
    return [doc.to_dict() for doc in docs]


# ── Reminders ────────────────────────────────────────────────────────────────

def create_reminder(caregiver_id: str, patient_id: str, data: dict) -> str:
    _assert_patient_owned(caregiver_id, patient_id)
    data["status"] = "pending"
    data["lastTriggeredAt"] = None
    data["createdAt"] = SERVER_TIMESTAMP
    doc_ref = (
        _patient_ref(caregiver_id, patient_id)
        .collection("reminders")
        .document()
    )
    doc_ref.set(data)
    return doc_ref.id


def get_reminders(caregiver_id: str, patient_id: str) -> list:
    _assert_patient_owned(caregiver_id, patient_id)
    docs = (
        _patient_ref(caregiver_id, patient_id)
        .collection("reminders")
        .stream()
    )
    return [{**doc.to_dict(), "reminderId": doc.id} for doc in docs]


def update_reminder(caregiver_id: str, patient_id: str, reminder_id: str, data: dict):
    _assert_patient_owned(caregiver_id, patient_id)
    ref = (
        _patient_ref(caregiver_id, patient_id)
        .collection("reminders")
        .document(reminder_id)
    )
    doc = ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Reminder not found.")
    data["updatedAt"] = SERVER_TIMESTAMP
    ref.update(data)


def get_reminders_since(caregiver_id: str, patient_id: str, since: datetime) -> list:
    """Returns all reminders updated/triggered since a given time (for adherence calc)."""
    docs = (
        _patient_ref(caregiver_id, patient_id)
        .collection("reminders")
        .where("createdAt", ">=", since)
        .stream()
    )
    return [doc.to_dict() for doc in docs]


# ── Engagement Summary ────────────────────────────────────────────────────────

def upsert_engagement_summary(caregiver_id: str, patient_id: str, data: dict):
    """
    Writes to engagementSummary/current.
    This is a backend-owned derived doc — never called directly by clients.
    """
    data["updatedAt"] = SERVER_TIMESTAMP
    (
        _patient_ref(caregiver_id, patient_id)
        .collection("engagementSummary")
        .document("current")
        .set(data, merge=True)
    )


def get_engagement_summary(caregiver_id: str, patient_id: str) -> dict | None:
    doc = (
        _patient_ref(caregiver_id, patient_id)
        .collection("engagementSummary")
        .document("current")
        .get()
    )
    return doc.to_dict() if doc.exists else None