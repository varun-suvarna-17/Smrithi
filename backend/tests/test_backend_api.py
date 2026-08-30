import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure backend directory is on sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.main import app
from app.database.db import db

@pytest.fixture(scope="module")
def client():
    # Reset in-memory database and seed demo data
    db.reset_for_testing()
    from app.main import seed_initial_demo_data
    seed_initial_demo_data()
    
    with TestClient(app) as c:
        yield c

# ----------------- 1. Health Check Test -----------------
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["total_games_supported"] == 5
    assert "docs_url" in data

# ----------------- 2. Authentication Tests -----------------
def test_auth_registration_and_login(client):
    # Register caregiver
    reg_payload = {
        "email": "test.caregiver@example.com",
        "password": "securepassword123",
        "full_name": "Rina Das",
        "role": "caregiver",
        "phone": "+91-9876500001"
    }
    reg_res = client.post("/api/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    user_data = reg_res.json()
    assert user_data["email"] == "test.caregiver@example.com"
    assert user_data["full_name"] == "Rina Das"

    # Login
    login_payload = {
        "email": "test.caregiver@example.com",
        "password": "securepassword123"
    }
    login_res = client.post("/api/auth/login", json=login_payload)
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # Verify /me endpoint
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "test.caregiver@example.com"

# ----------------- 3. Patient Management Tests -----------------
def test_patient_crud(client):
    patient_payload = {
        "name": "Nipen Borah",
        "age": 78,
        "gender": "Male",
        "dementia_stage": "Early Stage",
        "preferred_language": "as",
        "emergency_contact": "+91-9876543210",
        "medical_notes": "Mild MCI, loves Assam tea and traditional crafts.",
        "baseline_mmse_score": 25
    }
    create_res = client.post("/api/patients/", json=patient_payload)
    assert create_res.status_code == 201
    p_data = create_res.json()
    patient_id = p_data["id"]
    assert p_data["name"] == "Nipen Borah"
    assert p_data["current_difficulty_levels"]["memory"] == 1

    # Get patient
    get_res = client.get(f"/api/patients/{patient_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == patient_id

    # Update patient
    update_res = client.put(f"/api/patients/{patient_id}", json={"age": 79, "medical_notes": "Updated notes"})
    assert update_res.status_code == 200
    assert update_res.json()["age"] == 79

# ----------------- 4. Caregiver Association Tests -----------------
def test_caregiver_association(client):
    cg_payload = {
        "name": "Priyanka Sarma",
        "relationship": "Daughter",
        "phone": "+91-9123456789",
        "email": "priyanka.sarma@example.com"
    }
    cg_res = client.post("/api/caregivers/", json=cg_payload)
    assert cg_res.status_code == 201
    cg_id = cg_res.json()["id"]

    # Link with patient P001
    link_res = client.post("/api/caregivers/associate", json={"patient_id": "P001", "caregiver_id": cg_id})
    assert link_res.status_code == 200
    assert link_res.json()["success"] is True

    # Check assigned patients list
    assigned_res = client.get(f"/api/caregivers/{cg_id}/patients")
    assert assigned_res.status_code == 200
    assigned_patients = assigned_res.json()
    assert any(p["id"] == "P001" for p in assigned_patients)

# ----------------- 5. Cognitive Games Tests -----------------
def test_cognitive_games_flow(client):
    # List games
    games_res = client.get("/api/games/")
    assert games_res.status_code == 200
    games = games_res.json()
    assert len(games) == 5
    game_types = [g["id"] for g in games]
    assert "memory" in game_types
    assert "attention" in game_types
    assert "sequence" in game_types
    assert "pattern" in game_types
    assert "recognition" in game_types

    # Start memory game for P001
    start_payload = {
        "patient_id": "P001",
        "game_type": "memory",
        "difficulty_level": 2,
        "language": "as"
    }
    start_res = client.post("/api/games/start", json=start_payload)
    assert start_res.status_code == 200
    session_data = start_res.json()
    assert session_data["game_type"] == "memory"
    assert len(session_data["rounds_data"]) > 0
    assert "session_id" in session_data

    # Submit game attempt
    attempt_payload = {
        "patient_id": "P001",
        "session_id": session_data["session_id"],
        "game_type": "memory",
        "difficulty_level": 2,
        "score": 4,
        "total_questions": 4,
        "correct_answers": 4,
        "response_time_ms": 3100,
        "mistakes": 0,
        "attempts": 1,
        "session_duration_seconds": 50
    }
    submit_res = client.post("/api/games/submit-result", json=attempt_payload)
    assert submit_res.status_code == 201
    result_data = submit_res.json()
    assert result_data["accuracy"] == 100.0
    assert result_data["next_recommended_difficulty"] in [2, 3]

    # Get game history
    history_res = client.get("/api/games/attempts/P001")
    assert history_res.status_code == 200
    assert len(history_res.json()) >= 1

# ----------------- 6. Adaptive Difficulty Logic Tests -----------------
def test_adaptive_difficulty_progression(client):
    eval_req = {
        "patient_id": "P001",
        "game_type": "memory",
        "current_difficulty": 2
    }
    eval_res = client.post("/api/adaptive/evaluate", json=eval_req)
    assert eval_res.status_code == 200
    data = eval_res.json()
    assert "action" in data
    assert "confidence_score" in data
    assert "rationale" in data
    assert data["metrics"]["rolling_accuracy"] >= 0.0

# ----------------- 7. Analytics & Progress Tests -----------------
def test_analytics_and_domain_breakdown(client):
    analytics_res = client.get("/api/analytics/P001")
    assert analytics_res.status_code == 200
    data = analytics_res.json()
    assert data["patient_id"] == "P001"
    assert "domain_breakdown" in data
    assert "Memory" in data["domain_breakdown"]
    assert "improvement_indicators" in data
    assert "consistency_index" in data["improvement_indicators"]

    domain_res = client.get("/api/analytics/P001/domain-breakdown")
    assert domain_res.status_code == 200
    assert "domain_breakdown" in domain_res.json()

# ----------------- 8. Multilingual & NER Language Tests -----------------
def test_multilingual_endpoints(client):
    # List languages
    lang_res = client.get("/api/languages")
    assert lang_res.status_code == 200
    langs = lang_res.json()
    assert len(langs) >= 8
    codes = [l["code"] for l in langs]
    assert "as" in codes
    assert "bn" in codes
    assert "mni" in codes
    assert "brx" in codes

    # Get Assamese localized content
    as_res = client.get("/api/languages/content/as")
    assert as_res.status_code == 200
    as_data = as_res.json()
    assert "common_prompts" in as_data
    assert "game_vocabulary" in as_data
    assert "japi" in as_data["game_vocabulary"]

    # Translation
    trans_res = client.post("/api/languages/translate", json={
        "text": "Welcome to Smrithi Cognitive Memory Exercise",
        "source_language": "en",
        "target_language": "as"
    })
    assert trans_res.status_code == 200
    assert trans_res.json()["target_language"] == "as"

# ----------------- 9. Voice & TTS Tests -----------------
def test_voice_synthesis(client):
    voice_payload = {
        "text": "Remember these traditional objects",
        "language": "en",
        "speed_rate": 1.0
    }
    voice_res = client.post("/api/voice/synthesize", json=voice_payload)
    assert voice_res.status_code == 200
    v_data = voice_res.json()
    assert "format" in v_data
    assert v_data["duration_estimate_seconds"] > 0

# ----------------- 10. Reminders Tests -----------------
def test_reminders_crud(client):
    rem_payload = {
        "patient_id": "P001",
        "title": "Evening Tea & Memory Game",
        "message": "Time for your evening routine game.",
        "reminder_type": "cognitive_game",
        "scheduled_time": "2026-08-29T17:30:00",
        "recurring": True,
        "frequency": "daily"
    }
    create_res = client.post("/api/reminders", json=rem_payload)
    assert create_res.status_code == 201
    rem_id = create_res.json()["id"]

    # Get reminders
    list_res = client.get("/api/reminders/patient/P001")
    assert list_res.status_code == 200
    assert any(r["id"] == rem_id for r in list_res.json())

    # Mark complete
    patch_res = client.patch(f"/api/reminders/{rem_id}/complete?completed=true")
    assert patch_res.status_code == 200
    assert patch_res.json()["is_completed"] is True

    # Delete reminder
    del_res = client.delete(f"/api/reminders/{rem_id}")
    assert del_res.status_code == 200

# ----------------- 11. AI Progress Report Tests -----------------
def test_ai_progress_report(client):
    report_res = client.get("/api/reports/patient/P001/progress-report?days=30")
    assert report_res.status_code == 200
    report = report_res.json()
    assert report["patient_id"] == "P001"
    assert "clinical_summary" in report
    assert "observed_strengths" in report
    assert "areas_to_watch" in report
    assert "disclaimer" in report
    assert "NOT a medical diagnosis" in report["disclaimer"]

# ----------------- 12. Error Handling & Validation Tests -----------------
def test_error_handling(client):
    # Non-existent patient
    res_404 = client.get("/api/patients/P_NONEXISTENT_999")
    assert res_404.status_code == 404
    assert res_404.json()["error_type"] == "HTTPException"

    # Validation error (age below minimum 40)
    invalid_patient = {
        "name": "Young Person",
        "age": 20,
        "preferred_language": "as"
    }
    res_422 = client.post("/api/patients/", json=invalid_patient)
    assert res_422.status_code == 422
    assert res_422.json()["error_type"] == "ValidationError"
