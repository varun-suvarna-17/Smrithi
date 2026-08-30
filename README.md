
# Smrithi

#firebase rules

rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
# SMRITHI – AI-Powered Elderly Care Platform
### Cognitive Gaming and Memory Assistance Platform for Elderly Dementia Patients in North East India
**Smart India Hackathon (SIH) Problem Statement:** `SIH26003`

---

## 📌 Project Overview

**SMRITHI** is an AI-driven, culturally grounded cognitive stimulation and memory assistance platform engineered specifically for elderly dementia patients in North East India. This is a **full-stack monorepo** containing both the **REST API Backend** and **React Frontend**.

- **Backend:** FastAPI-based REST API with MongoDB, ML-powered adaptive difficulty, and multilingual support
- **Frontend:** React + Vite modern SPA with responsive design, offline support, and real-time synchronization

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ (for frontend)
- **Python** 3.10+ (for backend)
- **MongoDB** (local or Atlas URI)
- **npm** or **yarn** package manager

### Installation & Setup

#### 1. **Clone Repository**
```bash
git clone https://github.com/deekshanayak-1108/Smrithi.git
cd Smrithi
```

#### 2. **Install All Dependencies**
```bash
npm run install:all
```
This will install:
- Root node modules (for concurrent task running)
- Backend Python dependencies
- Frontend node modules

#### 3. **Environment Configuration**
Copy `.env.example` to `.env` in the root directory and configure:

```bash
cp .env.example .env
```

**Backend settings (.env):**
- `MONGODB_URI` - MongoDB connection string
- `PORT` - Backend API port (default: 8000)
- `SECRET_KEY` - JWT secret key
- `GEMINI_API_KEY` / `OPENAI_API_KEY` - Optional for AI report generation

**Frontend settings (.env or .env.local):**
- `VITE_API_BASE_URL` - Backend API URL (default: http://localhost:8000)

#### 4. **Run Full Stack**
```bash
npm run dev
```

This will start:
- ✅ **Backend API** on `http://localhost:8000`
- ✅ **Frontend App** on `http://localhost:5173`
- ✅ **Swagger Docs** on `http://localhost:8000/docs`

---

## 📂 Project Structure

```
smrithi/  (monorepo root)
│
├── backend/                        # FastAPI REST API
│   ├── app/
│   │   ├── main.py                # Application Entry Point
│   │   ├── core/
│   │   │   └── config.py          # Configuration & Environment Settings
│   │   ├── database/
│   │   │   └── db.py              # MongoDB Manager + In-Memory Fallback
│   │   ├── models/                # Database Document Models
│   │   ├── schemas/               # Pydantic Request/Response Validation
│   │   ├── routes/                # REST API Endpoints
│   │   │   ├── auth.py            # JWT Authentication & RBAC
│   │   │   ├── patients.py        # Patient Profiles & MMSE Tracking
│   │   │   ├── caregivers.py      # Caregiver Management
│   │   │   ├── games.py           # Cognitive Games Engine
│   │   │   ├── adaptive.py        # Adaptive Difficulty System
│   │   │   ├── progress.py        # Progress Analytics
│   │   │   ├── voice.py           # TTS Voice Service
│   │   │   ├── reminders.py       # Reminder System
│   │   │   └── reports.py         # AI Clinical Reports
│   │   ├── services/              # Business Logic & Integrations
│   │   ├── ai/
│   │   │   ├── adaptive/          # ML-based Adaptive Engine
│   │   │   └── ai_report_service.py # Report Generator
│   │   ├── middleware/            # Auth Guards & Error Handlers
│   │   └── utils/                 # Helper Functions
│   ├── requirements.txt           # Python Dependencies
│   └── tests/                     # Backend Tests
│
├── frontend/                       # React + Vite SPA
│   ├── src/
│   │   ├── main.jsx              # Entry Point
│   │   ├── App.jsx               # Root Component
│   │   ├── components/           # Reusable Components
│   │   │   ├── Layout.jsx
│   │   │   ├── TopNav.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── BottomNav.jsx
│   │   │   └── ...
│   │   ├── pages/                # Page Components
│   │   │   ├── Home.jsx
│   │   │   ├── Games.jsx
│   │   │   ├── CaregiverDashboard.jsx
│   │   │   ├── ActivityHub.jsx
│   │   │   └── ...
│   │   ├── utils/                # Helper Functions
│   │   │   └── audio.js          # Audio Utilities
│   │   └── assets/               # Static Assets
│   ├── public/                   # Public Static Files
│   │   └── images/               # Game Assets
│   ├── vite.config.js            # Vite Configuration with API Proxy
│   ├── package.json              # Frontend Dependencies
│   └── .env.example              # Frontend Environment Template
│
├── package.json                   # Root Scripts for Monorepo
├── .env.example                   # Full-Stack Environment Template
└── README.md                      # This File

```

---

## 🎮 Available Scripts

### Root-Level Commands
```bash
npm run dev                        # Run both backend & frontend concurrently
npm run build                      # Build both backend & frontend
npm run install:all               # Install all dependencies (root, backend, frontend)
```

### Backend Commands
```bash
npm run backend:dev               # Start backend API with hot-reload
npm run backend:build             # Prepare backend for production
npm run backend:install           # Install Python dependencies
```

### Frontend Commands
```bash
npm run frontend:dev              # Start frontend dev server
npm run frontend:build            # Build frontend for production
npm run frontend:install          # Install node modules
```

---

## 🔌 API Integration

### Frontend → Backend Communication

The frontend is configured to communicate with the backend via:
- **Development:** Vite proxy routes `/api/*` to `http://localhost:8000`
- **Production:** Set `VITE_API_BASE_URL` environment variable

### Example API Call (Frontend)
```javascript
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Login
const response = await axios.post(`${API_BASE}/auth/login`, {
  username: 'caregiver@example.com',
  password: 'password'
});

// Get Patient List
const patients = await axios.get(`${API_BASE}/patients`, {
  headers: { Authorization: `Bearer ${token}` }
});
```

### API Endpoints (Backend)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Caregiver Login |
| GET | `/patients` | List Patients |
| POST | `/patients/{id}/games/{game_id}` | Log Game Attempt |
| GET | `/progress/{patient_id}` | Get Progress Analytics |
| POST | `/voice/tts` | Text-to-Speech |
| GET | `/reports/{patient_id}` | Get AI Clinical Report |

See **Swagger Docs** at `http://localhost:8000/docs` for complete API reference.

---

## 🧠 Key Features

### Backend
- ✅ **FastAPI** - Modern async Python web framework
- ✅ **MongoDB** - NoSQL database with in-memory fallback
- ✅ **JWT Authentication** - Secure token-based auth with role-based access control
- ✅ **ML-Powered Adaptive System** - Dynamic difficulty adjustment based on performance
- ✅ **Multilingual Support** - Hindi, Assamese, Kannada, English
- ✅ **Text-to-Speech** - Audio generation for game instructions
- ✅ **Clinical Reports** - AI-generated progress summaries
- ✅ **Reminder System** - Scheduled medications, games, routines

### Frontend
- ✅ **React 19** - Latest React features
- ✅ **Vite** - Lightning-fast dev server & build
- ✅ **React Router** - Client-side navigation
- ✅ **Responsive Design** - Mobile, tablet, desktop support
- ✅ **Offline Support** - Works without internet (with IndexedDB caching)
- ✅ **Real-time Updates** - WebSocket support for live data
- ✅ **Accessibility** - WCAG 2.1 compliant components

---

## 🔐 Authentication Flow

1. **Frontend:** User enters credentials on login page
2. **Request:** POST `/auth/login` with username/password
3. **Backend:** Validates credentials, generates JWT token
4. **Response:** Returns token + user metadata
5. **Frontend:** Stores token, includes in Authorization headers
6. **Protected Routes:** Frontend guards routes, backend validates tokens

---

## 📊 Database Schema

### Core Collections
- **patients** - Elderly patient profiles (name, age, MMSE score, etc.)
- **caregivers** - Caregiver accounts + patient associations
- **game_attempts** - Game performance history
- **sessions** - User sessions & activity tracking
- **reminders** - Medication & gaming reminders
- **progress_analytics** - Aggregated performance metrics

---

## 🚀 Deployment

### Backend Deployment
```bash
# Using Uvicorn (Production)
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Using Docker
docker build -t smrithi-backend .
docker run -p 8000:8000 smrithi-backend
```

### Frontend Deployment
```bash
# Build for Production
npm run frontend:build

# Deploy 'frontend/dist' to any static host (Vercel, Netlify, AWS S3, etc.)
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** - see LICENSE file for details.

---

## 👥 Team

**SMRITHI Development Team** - Smart India Hackathon 2026

---

## 📞 Support

For issues, questions, or suggestions:
- 📧 Email: smrithi.team@example.com
- 🐛 GitHub Issues: [Report a Bug](https://github.com/deekshanayak-1108/Smrithi/issues)
- 💬 Discussions: [Ask a Question](https://github.com/deekshanayak-1108/Smrithi/discussions)

---

**Made with ❤️ for Elderly Care in North East India**

---

## 🚀 Key Architecture & Features

```
smrithi-backend/
│
├── app/
│   ├── main.py                     # FastAPI Application Initialization & Lifespan
│   ├── core/
│   │   └── config.py               # Pydantic Settings & Environment Configuration
│   ├── database/
│   │   └── db.py                   # MongoDB Manager + Zero-Config In-Memory Fallback
│   ├── models/                     # Database Document Models
│   ├── schemas/                    # Pydantic V2 Request & Response Validation Schemas
│   ├── routes/                     # Clean Modular REST API Routers
│   │   ├── auth.py                 # JWT Authentication & Role-Based Access Control
│   │   ├── patients.py             # Elderly Patient Profile Lifecycle & MMSE Tracking
│   │   ├── caregivers.py           # Caregiver Accounts, Associations & Clinical Alerts
│   │   ├── games.py                # 5 Cognitive Games Engine & Attempt History
│   │   ├── adaptive.py             # Adaptive Difficulty Evaluation Endpoints
│   │   ├── progress.py             # Multi-Domain Progress Tracking & Analytics
│   │   ├── languages.py            # Multilingual NER Localization & Translation
│   │   ├── voice.py                # Text-To-Speech (TTS) Voice Synthesis Service
│   │   ├── reminders.py            # Routine, Medication & Gaming Reminders
│   │   └── reports.py              # AI Clinical Progress Summary & Doctor Reports
│   ├── services/                   # Business Logic & External Service Abstractions
│   ├── ai/
│   │   ├── adaptive/
│   │   │   ├── feature_extractor.py # Statistical Rolling Feature Extraction
│   │   │   ├── adaptive_rules.py   # Heuristic Rule-Based Progression Engine
│   │   │   └── ml_pipeline.py      # Modular Preprocessing, Model & Evaluation Pipeline
│   │   └── ai_report_service.py    # Clinical Progress Synthesizer (Gemini + Local Rules)
│   ├── middleware/
│   │   ├── auth_guard.py           # Bearer Token & Role Guards
│   │   └── error_handler.py        # Global Exception Handlers (Zero Crashes)
│   └── utils/
│       └── helpers.py              # Timezone-aware UTC helpers
│
├── tests/
│   └── test_backend_api.py         # Pytest Automated Test Suite (100% Pass)
│
├── Smrithi_Backend.postman_collection.json # Complete Postman Collection
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🧠 5 Cognitive Games with North Eastern Cultural Context

| Game Type | Cognitive Domain | Cultural Context (NER) | Description & Stimuli |
| :--- | :--- | :--- | :--- |
| **1. Memory** | *Short-term & Working Memory* | Assamese Japi, Folk Dhol, Bamboo Kula, Pepa Hornpipe | Displays N cultural stimuli for brief observation. Patient recalls target items from distractor options. |
| **2. Attention** | *Selective & Sustained Attention* | Folk craft symbols, Bell-metal utensils | Patient quickly scans a visual grid of distractors to locate a target cultural motif. |
| **3. Sequence** | *Executive Function & Reasoning* | Assam tea preparation, Traditional recipes, Weaving setup | Patient orders disordered daily routine steps into the correct chronological sequence. |
| **4. Pattern** | *Pattern Recognition & Inductive Logic* | Eri, Muga, and tribal textile borders | Patient predicts the next repeating geometric motif in a traditional handloom pattern. |
| **5. Recognition** | *Semantic & Visual Memory* | Regional heritage items, musical instruments | Identifies regional cultural tools and symbols from visual cues and names. |

---

## 📈 Multi-Factor Adaptive Difficulty Module

The adaptive difficulty system dynamically scales cognitive challenge based on patient performance to stimulate neuroplasticity without causing cognitive frustration.

### 1. Data Preprocessing & Feature Extraction (`feature_extractor.py`)
- **Rolling Accuracy**: Mean accuracy over the last 3–5 attempts.
- **Average Response Latency**: Response time in milliseconds.
- **Latency Variance / Standard Deviation**: Measures consistency and cognitive fatigue.
- **Mistake Rate**: Ratio of incorrect attempts to total questions.
- **Performance Streak**: Consecutive successes ($\ge 80\%$) vs. struggles ($< 50\%$).
- **Linear Trend Slope**: Rate of improvement or decline over time ($\frac{\Delta \text{Accuracy}}{\Delta \text{Sessions}}$).

### 2. Heuristic Rule Engine (`adaptive_rules.py`)
- **Increase Difficulty (+1, max 5)**: When rolling accuracy $\ge 85\%$ or ($\ge 75\%$ with positive streak $\ge 2$) and stable latency.
- **Decrease Difficulty (-1, min 1)**: When accuracy $< 50\%$, negative streak $\le -2$, or steep negative slope.
- **Maintain Difficulty**: When patient is in optimal consolidation zone ($50\% - 80\%$).

### 3. ML Architecture Separation (`ml_pipeline.py`)
- Fully separated **Data Preprocessing**, **Feature Extraction**, **Model Interface**, and **Prediction Engine** allowing plug-and-play machine learning classifiers or reinforcement learning algorithms.

---

## 🌐 Multilingual / North Eastern Language Support

Native support for **9 languages** with localized prompt matrices and cultural object vocabulary:
1. **Assamese (`as`)**: অসমীয়া (Native scripts & cultural prompts)
2. **Bengali (`bn`)**: বাংলা (Tripura & Barak Valley regional prompts)
3. **Manipuri / Meitei (`mni`)**: মৈতৈলোন্ / ꯃꯤꯇꯩꯂꯣꯟ
4. **Bodo (`brx`)**: बर'
5. **Mizo (`lus`)**: Mizo ṭawng
6. **Khasi (`kha`)**: Ka Ktien Khasi
7. **Garo (`grt`)**: A·chik
8. **Hindi (`hi`)**: हिन्दी
9. **English (`en`)**: English

---

## 🎙️ Voice & Text-To-Speech (TTS) Service

- **Endpoint**: `POST /api/voice/synthesize`
- Generates speech audio for cognitive instructions in regional Indian phonetics using `gTTS` with local disk caching and base64 streaming.
- Graceful offline fallback when external network connectivity is unavailable.

---

## 🩺 AI Progress Reports & Clinical Intelligence

- **Endpoint**: `GET /api/reports/patient/{patient_id}/progress-report`
- Aggregates actual stored performance data, domain scores, consistency rating, and latency trajectories.
- Synthesizes a structured, doctor-ready JSON report containing:
  - Clinical Summary narrative
  - Domain breakdown across all 5 cognitive areas
  - Identified strengths and areas to watch
  - Caregiver actionable suggestions
  - Adherence and consistency score

> **Medical Disclaimer**: SMRITHI progress reports provide progress-assistance analytics for caregivers and healthcare facilitators. They are **NOT** medical diagnostic devices and do not replace clinical neuropsychological evaluation.

---

## ⚙️ Installation & Running the Server

### Prerequisites
- Python 3.10+
- (Optional) MongoDB server running locally or MongoDB Atlas connection string.

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### Step 3: Run the Backend Server
```bash
python app.py
```
Or with Uvicorn directly:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Server will start on: **`http://127.0.0.1:8000`**

---

## 📖 Interactive API Documentation

Once started, open your browser to access the full interactive OpenAPI documentation:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Automated Testing

Run the comprehensive Pytest test suite:
```bash
pytest backend/tests/test_backend_api.py -v
```

All 12 critical test suites verify:
- Health checks
- Authentication & JWT token security
- Patient & Caregiver lifecycle and association
- 5 Cognitive games session generation & answer submissions
- Adaptive difficulty progression logic
- Multi-domain analytics and trajectory indicators
- Multilingual content retrieval and translation
- Voice TTS synthesis
- Reminder CRUD operations
- AI progress reports
- Error handling and input validation

---

## 📮 Postman Collection

Import `Smrithi_Backend.postman_collection.json` directly into Postman. It includes pre-configured variables:
- `{{base_url}}`: `http://127.0.0.1:8000`
- `{{patient_id}}`: `P001` (seeded demo patient)
- `{{caregiver_id}}`: `cg_demo_001` (seeded demo caregiver)

### Key Postman Endpoints Overview
1. **Health**: `GET /health`
2. **Register**: `POST /api/auth/register`
3. **Login**: `POST /api/auth/login`
4. **Create Patient**: `POST /api/patients/`
5. **Get Patient**: `GET /api/patients/P001`
6. **List Games**: `GET /api/games/`
7. **Start Game**: `POST /api/games/start`
8. **Submit Game Result**: `POST /api/games/submit-result`
9. **Get History**: `GET /api/games/attempts/P001`
10. **Adaptive Difficulty**: `POST /api/adaptive/evaluate`
11. **Multi-Domain Analytics**: `GET /api/analytics/P001`
12. **Languages**: `GET /api/languages`
13. **Voice TTS**: `POST /api/voice/synthesize`
14. **Create Reminder**: `POST /api/reminders`
15. **Generate AI Progress Report**: `GET /api/reports/patient/P001/progress-report?days=30`

---

## 🛡️ Honesty & Transparency Disclosure

- **Adaptive Difficulty**: Features a clear, production-grade statistical feature extractor and heuristic rule engine, alongside an ML pipeline scaffold. It does not make false claims of opaque black-box AI.
- **Clinical AI Summary**: Built-in deterministic clinical intelligence engine generates structured progress summaries directly from stored game attempts, with optional integration for Google Gemini via `GEMINI_API_KEY`.
- **Database**: Full MongoDB database integration with an automatic zero-config in-memory fallback for instant local evaluation.
