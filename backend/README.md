# SMRITHI – Backend REST API
### AI-Based Cognitive Gaming and Memory Assistance Platform for Elderly Dementia Patients in the North Eastern Region (NER)
**Smart India Hackathon (SIH) Problem Statement:** `SIH26003`

This is the FastAPI-based backend for the SMRITHI cognitive care platform. It handles elderly patient and caregiver management, session tracking, daily checklists, medicine reminders, and a localized text-to-speech (TTS) voice layer. It uses **Firebase / Firestore** as the database and identity provider.

---

## 🛠️ Prerequisites & Setup

### 1. Requirements
* **Python**: Version 3.10 or higher
* **gTTS**: Installed automatically via requirements (used for localized voice prompts)

### 2. Environment Virtualization
Create and activate a Python virtual environment, then install dependencies:
```bash
# Navigate to backend directory
cd backend/

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/bin/activate  # Linux/macOS
# or
venv\Scripts\activate          # Windows

# Install required dependencies
pip install -r requirements.txt
```

---

## 🔥 Firebase & Firestore Configuration

This backend requires connection credentials to initialize the Firebase Admin SDK. Follow these steps to configure your project database:

### 1. Setup Firebase Console
1. Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project.
2. Under **Build**, select **Authentication** and enable the **Email/Password** sign-in provider.
3. Select **Firestore Database** and click **Create Database** (start in native mode).

### 2. Get Private Key Credentials (JSON File)
To authenticate the backend server with your database:
1. Open the Firebase Console and go to **Project Settings** (gear icon) ➔ **Service Accounts**.
2. Click the **"Generate new private key"** button at the bottom.
3. A JSON file will download. Rename this file to:
   ```text
   backend/serviceAccountKey.json
   ```
   *(Note: This file is already configured in `.gitignore` to prevent committing your private keys to Git).*

### 3. Firestore Security Rules
Security rules for Firestore are located at the root of this repository in `firestore.rules`. You can deploy these rules to Firestore via the Firebase CLI using:
```bash
firebase deploy --only firestore:rules
```

---

## 🚀 Running the Backend

Ensure your virtual environment is active, then run:

```bash
# Run via launcher entry point
python app.py
```
Or directly via uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

* **Interactive API Documentation (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **Health Endpoint**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 🧪 Testing the API

### Automated Smoke Tests
A comprehensive 22-step integration check is provided. Once your Firebase credential JSON file is placed:
1. Open [`backend/.env`](.env) and add your `FIREBASE_WEB_API_KEY` (needed by the test to obtain mock ID tokens).
2. Run the smoke test suite:
   ```bash
   python ../scripts/smoke_test.py
   ```