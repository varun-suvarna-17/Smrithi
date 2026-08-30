"""
SPARSH Backend — Automated Smoke Test
======================================
Runs the full Definition-of-Done flow from PRD §8 automatically.
The human should not need to run curl commands by hand once this exists.

Usage (from the repo root):
    python scripts/smoke_test.py

Prerequisites:
    - FastAPI server running locally:  uvicorn app.main:app --app-dir backend --reload
    - .env must contain FIREBASE_WEB_API_KEY
    - FIREBASE_PROJECT_ID, FIREBASE_CLIENT_EMAIL, FIREBASE_PRIVATE_KEY already set

STOP CHECKPOINTS are printed as [STOP] — do NOT proceed past them without reading them.
"""

import os
import sys
import json
import datetime
from datetime import timezone
import certifi
import requests
from dotenv import load_dotenv

# ── Fix: PostgreSQL installs a broken CA bundle path that clobbers SSL_CERT_FILE.
# Force requests (and urllib3) to use certifi's own bundle instead.
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()

# Load .env from repo root or backend/
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# ── Config ────────────────────────────────────────────────────────────────────
API_BASE = os.getenv("SMOKE_TEST_API_BASE", "http://localhost:8000")
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY", "")
FIREBASE_AUTH_REST = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
STOP = "\033[93m[STOP]\033[0m"

results: list[tuple[str, bool, str]] = []


def check(name: str, passed: bool, detail: str = ""):
    status = PASS if passed else FAIL
    print(f"  {status}  {name}" + (f" — {detail}" if detail else ""))
    results.append((name, passed, detail))


def stop(message: str):
    """Print a manual checkpoint and exit. Do NOT skip past these."""
    print(f"\n{STOP} MANUAL CHECKPOINT REQUIRED\n")
    print(f"  {message}\n")
    sys.exit(0)


# ── Pre-flight checks ─────────────────────────────────────────────────────────

def preflight():
    print("\n=== Pre-flight checks ===")

    if not FIREBASE_WEB_API_KEY:
        stop(
            "FIREBASE_WEB_API_KEY is not set in .env.\n"
            "  The smoke test signs up test users via Firebase Auth REST, which needs this key.\n"
            "  Find it in: Firebase Console → Project Settings → General → Web API Key.\n"
            "  Add it to .env as:  FIREBASE_WEB_API_KEY=AIza..."
        )

    try:
        r = requests.get(f"{API_BASE}/health", timeout=5)
        check("/health responds", r.status_code == 200, f"status={r.status_code}")
    except requests.exceptions.ConnectionError:
        stop(
            f"Cannot reach FastAPI server at {API_BASE}.\n"
            "  Start it first:  uvicorn app.main:app --app-dir backend --reload\n"
            "  Or set SMOKE_TEST_API_BASE=http://your-host:port"
        )


# ── Firebase Auth REST helpers ─────────────────────────────────────────────────

def signup_caregiver(email: str, password: str) -> str:
    """Signs up a new caregiver via Firebase Auth REST and returns the idToken."""
    resp = requests.post(
        f"{FIREBASE_AUTH_REST}?key={FIREBASE_WEB_API_KEY}",
        json={"email": email, "password": password, "returnSecureToken": True},
        timeout=10,
    )
    if resp.status_code != 200:
        print(f"    Firebase Auth signup failed: {resp.text}")
        return ""
    return resp.json().get("idToken", "")


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ── Test flows ────────────────────────────────────────────────────────────────

def test_auth():
    print("\n=== 1. Firebase Auth — sign up two test caregivers ===")

    ts = datetime.datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    email1 = f"smoke_cg1_{ts}@test.sparsh"
    email2 = f"smoke_cg2_{ts}@test.sparsh"
    pw = "TestPass123!"

    token1 = signup_caregiver(email1, pw)
    check("Caregiver 1 signup", bool(token1), email1)

    token2 = signup_caregiver(email2, pw)
    check("Caregiver 2 signup", bool(token2), email2)

    if not token1 or not token2:
        stop(
            "Could not obtain Firebase ID tokens. Check FIREBASE_WEB_API_KEY and that "
            "Email/Password auth is enabled in the Firebase console."
        )

    return token1, token2


def test_no_auth():
    print("\n=== 2. Reject unauthenticated request ===")
    r = requests.post(f"{API_BASE}/api/patients", json={"name": "X", "age": 70, "contentLanguage": "en"})
    check("POST /api/patients without token → 403/401/422", r.status_code in (401, 403, 422))


def test_crud(token1: str) -> str:
    print("\n=== 3. Full CRUD flow (caregiver 1) ===")

    # Create patient
    r = requests.post(
        f"{API_BASE}/api/patients",
        json={"name": "Aita Bora", "age": 72, "contentLanguage": "as"},
        headers=auth_headers(token1),
    )
    check("POST /api/patients → 201", r.status_code == 201, f"status={r.status_code}")
    patient_id = r.json().get("patientId", "") if r.status_code == 201 else ""
    check("patientId returned", bool(patient_id))

    if not patient_id:
        check("Skipping remaining CRUD — no patientId", False)
        return ""

    # Get patient
    r = requests.get(f"{API_BASE}/api/patients/{patient_id}", headers=auth_headers(token1))
    check("GET /api/patients/{id} → 200", r.status_code == 200)

    # Patch patient
    r = requests.patch(
        f"{API_BASE}/api/patients/{patient_id}",
        json={"contentLanguage": "kha"},
        headers=auth_headers(token1),
    )
    check("PATCH /api/patients/{id} → 200", r.status_code == 200)

    # Post a session
    now = datetime.datetime.utcnow()
    session_body = {
        "gameType": "memory_recall",
        "startedAt": now.isoformat() + "Z",
        "endedAt": (now + datetime.timedelta(minutes=4)).isoformat() + "Z",
        "completed": True,
        "languageUsed": "kha",
        "difficultyLevel": 2,
        "correctCount": 7,
        "wrongCount": 3,
        "difficultyDropped": True,
    }
    r = requests.post(
        f"{API_BASE}/api/patients/{patient_id}/sessions",
        json=session_body,
        headers=auth_headers(token1),
    )
    check("POST /sessions → 201", r.status_code == 201, f"status={r.status_code}")

    if r.status_code == 201:
        body = r.json()
        check("sessionId in response", "sessionId" in body)
        check("engagementSummary in response", "engagementSummary" in body)
        es = body.get("engagementSummary", {})
        check("streakCount >= 1", es.get("streakCount", 0) >= 1, str(es.get("streakCount")))
        check("weeklySessionCount >= 1", es.get("weeklySessionCount", 0) >= 1)

    # Get session list
    r = requests.get(f"{API_BASE}/api/patients/{patient_id}/sessions", headers=auth_headers(token1))
    check("GET /sessions → 200", r.status_code == 200)
    check("sessions list non-empty", len(r.json()) >= 1 if r.status_code == 200 else False)

    # Create reminder
    r = requests.post(
        f"{API_BASE}/api/patients/{patient_id}/reminders",
        json={"type": "medicine", "title": "Evening tablet", "scheduledTime": "19:00", "recurrence": "daily"},
        headers=auth_headers(token1),
    )
    check("POST /reminders → 201", r.status_code == 201)
    reminder_id = r.json().get("reminderId", "") if r.status_code == 201 else ""

    # List reminders
    r = requests.get(f"{API_BASE}/api/patients/{patient_id}/reminders", headers=auth_headers(token1))
    check("GET /reminders → 200", r.status_code == 200)

    # Patch reminder status
    if reminder_id:
        r = requests.patch(
            f"{API_BASE}/api/patients/{patient_id}/reminders/{reminder_id}",
            json={"status": "completed"},
            headers=auth_headers(token1),
        )
        check("PATCH /reminders/{id} → 200", r.status_code == 200)
        if r.status_code == 200:
            es = r.json().get("engagementSummary", {})
            check("adherenceRate in summary after reminder update", "reminderAdherenceRate" in es)

    # Dashboard fallback
    r = requests.get(f"{API_BASE}/api/patients/{patient_id}/dashboard", headers=auth_headers(token1))
    check("GET /dashboard → 200", r.status_code == 200)

    return patient_id


def test_cross_account(token2: str, patient_id: str):
    print("\n=== 4. Cross-account rejection (caregiver 2 accessing caregiver 1's patient) ===")

    if not patient_id:
        check("Skipped — no patientId from step 3", False)
        return

    r = requests.get(f"{API_BASE}/api/patients/{patient_id}", headers=auth_headers(token2))
    check(
        "GET caregiver1's patient with caregiver2's token → 403",
        r.status_code == 403,
        f"status={r.status_code}",
    )

    r = requests.post(
        f"{API_BASE}/api/patients/{patient_id}/sessions",
        json={
            "gameType": "memory_recall",
            "startedAt": datetime.datetime.utcnow().isoformat() + "Z",
            "completed": True,
            "languageUsed": "en",
            "difficultyLevel": 1,
            "correctCount": 3,
            "wrongCount": 1,
            "difficultyDropped": False,
        },
        headers=auth_headers(token2),
    )
    check(
        "POST session to caregiver1's patient with caregiver2's token → 403",
        r.status_code == 403,
        f"status={r.status_code}",
    )

    print(
        f"\n{STOP} Cross-account check above confirms rejection at the FastAPI layer.\n"
        "  It does NOT confirm Firestore security rules (the dashboard reads Firestore directly).\n"
        "  Action required:\n"
        "    1. Open caregiver 1's engagementSummary/current in the Firestore console.\n"
        "    2. Trigger a session POST.\n"
        "    3. Confirm the doc updates without a manual refresh (should be within ~1s).\n"
        "    4. Try reading caregiver 1's data from the console using caregiver 2's UID — confirm it's blocked.\n"
        "  (The agent cannot observe the Firestore console visually.)"
    )


# ── Firestore rules reminder ───────────────────────────────────────────────────

def remind_deploy_rules():
    print("\n=== Manual checkpoint: Firestore Security Rules ===")
    print(
        f"{STOP} firestore.rules has been written to the repo root.\n"
        "  You must deploy it yourself — the agent cannot authenticate to your Firebase project.\n"
        "  Option A (Firebase Console): Firestore → Rules tab → paste & publish.\n"
        "  Option B (CLI): firebase deploy --only firestore:rules\n"
        "  Until rules are deployed, Firestore data is protected only at the FastAPI layer."
    )


# ── Summary ───────────────────────────────────────────────────────────────────

def print_summary():
    print("\n" + "=" * 50)
    print("SMOKE TEST SUMMARY")
    print("=" * 50)
    passed = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    for name, ok, detail in results:
        status = PASS if ok else FAIL
        print(f"  {status}  {name}" + (f" ({detail})" if detail else ""))
    print(f"\nTotal: {passed} passed, {failed} failed")
    if failed == 0:
        print(f"\n{PASS} All automated checks passed.")
        print("See [STOP] checkpoints above for manual Firestore verification steps.")
    else:
        print(f"\n{FAIL} {failed} check(s) failed — review output above.")
    print("=" * 50 + "\n")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("SPARSH Backend Smoke Test")
    print(f"Target API: {API_BASE}")

    preflight()
    token1, token2 = test_auth()
    test_no_auth()
    patient_id = test_crud(token1)
    test_cross_account(token2, patient_id)
    remind_deploy_rules()
    print_summary()

