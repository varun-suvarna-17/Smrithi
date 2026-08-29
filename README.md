# Smrithi — Cognitive Gaming Backend Engine

> **SIH 2026 — Problem Statement SIH26003**: AI-Based Cognitive Gaming & Memory Assistance Platform for Elderly Dementia Patients in the North Eastern Region[cite: 1].

Smrithi provides a lightweight, localized cognitive gaming backend designed specifically for elderly dementia care in North East India[cite: 1]. The platform features rule-based adaptive difficulty adjustment and dynamic localized asset generation (supporting regional contexts such as Assamese and Khasi languages)[cite: 1].

---

## 🛠️ Tech Stack & Dependencies

* **Framework:** FastAPI (`v0.110.0`)[cite: 1]
* **Server:** Uvicorn (`v0.28.0`)[cite: 1]
* **Data Validation:** Pydantic (`v2.6.4`)[cite: 1]
* **Database & Cloud Integration:** `firebase-admin` (`v6.5.0`)[cite: 1]

---

## 🚀 Key Features & API Endpoints

* **Game Configuration Endpoint (`POST /api/games/config`)**  
  Generates localized game assets, audio prompts, and structured rules for the cognitive games (`memory_match`, `recognition`, `sequence_recall`, `motif_weaver`, `regional_kitchen`)[cite: 1].
* **Session Processing & Adaptive Engine (`POST /api/games/session`)**  
  Ingests active player metrics (tap count, accuracy, time taken, mistakes), records gameplay history, and dynamically adjusts the player's difficulty level (Levels 1–3)[cite: 1].
* **Patient Caregiver Summary (`GET /api/patients/{patient_id}/summary`)**  
  Retrieves a comprehensive progress summary including the patient's active settings, profile metrics, and lifetime gameplay logs[cite: 1].

---

## 📂 Project Structure

```text
Smrithi_backend_logic/
├── .gitignore
├── README.md
├── requirements.txt
└── main.py
```[cite: 1]

---

## 💻 Local Setup & Execution Guide

### 1. Prerequisites
Ensure you have **Python 3.9+** and **Git** installed on your system[cite: 1].

### 2. Environment Setup
Clone your forked repository and move into the backend project directory[cite: 1]:
```bash
git clone <your-repository-url>
cd Smrithi_backend_logic
```[cite: 1]

Create and activate a Python virtual environment:
* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```[cite: 1]
* **Linux / macOS:**
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```[cite: 1]

### 3. Install Requirements
Install all locked dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```[cite: 1]

### 4. Run Development Server
Start the Uvicorn ASGI server with live auto-reloading:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```[cite: 1]

Access interactive Swagger documentation at **`http://127.0.0.1:8000/docs`**[cite: 1].

---

## 📡 Sample API Request Payloads

### 1. Fetch Localized Game Configuration
`POST /api/games/config`[cite: 1]

```json
{
  "patient_id": "patient123",
  "game_type": "memory_match",
  "language": "as"
}
```[cite: 1]

### 2. Submit Gameplay Session
`POST /api/games/session`[cite: 1]

```json
{
  "patient_id": "patient123",
  "game_type": "memory_match",
  "difficulty_level": 1,
  "total_taps": 8,
  "correct_taps": 6,
  "mistakes": 2,
  "duration_seconds": 18.4
}
```[cite: 1]

### 3. Fetch Caregiver Dashboard Summary
`GET /api/patients/patient123/summary`[cite: 1]
