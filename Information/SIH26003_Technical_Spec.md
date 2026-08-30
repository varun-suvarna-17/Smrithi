# SPARSH — Technical Specification & Build Plan
### SIH26003 — AI-Based Cognitive Gaming & Memory Assistance Platform for NER

---

## 1. Technical Stack

### Phase 1 — Core MVP
| Layer | Choice | Notes |
|---|---|---|
| Frontend | React + Vite | Mobile-responsive web app; two route trees — patient play view (large UI) and caregiver control panel |
| Styling | Tailwind CSS | Enforces consistent large-tap-target, large-text elderly-friendly UI |
| Backend | FastAPI | Handles game logic, session data, caregiver controls |
| Database / Realtime sync | Firebase (Firestore) | Real-time sync so patient session completion reflects instantly on caregiver dashboard; accessible from FastAPI via `firebase-admin` SDK |
| Auth | Firebase Auth | Caregiver login; simple, no custom auth needed |
| Voice layer (output) | Pre-recorded regional-language audio prompts + Web Speech API (TTS) as fallback | One-way voice (narration/prompts) only — no live speech-to-text in Phase 1, since ASR reliability is a demo risk |
| Content/i18n | JSON config per language (`content/as.json`, `content/en.json`) | Config-driven — proves scalability to other NER languages without rebuilding |
| Hosting | Firebase Hosting / Vercel | Fast deploy for demo |

### Phase 2 — Post-Basic-MVP Enhancements
| Layer | Choice | Notes |
|---|---|---|
| ML — Performance Report | scikit-learn (logistic regression / decision tree) | Trained on synthetic session data; classifies trend per cognitive domain (improving/stable/declining); outputs doctor-reviewable report |
| ML — Personalized Content | LLM API call | Caregiver inputs family facts (names, hometown, festival, memory) once at setup → LLM generates personalized memory-recall questions |
| Voice enhancement | Explore speech-to-text for answer input | Only after core MVP is stable and demo-reliable; flagged as a live-demo risk, so build and test thoroughly before relying on it |
| Adaptive difficulty | Rule-based auto-adjust within caregiver-set bounds | Future layer on top of manual caregiver control |

---

## 2. System Architecture (Overview)

```
[Patient Web View] ──plays game──> [FastAPI Backend] ──writes session data──> [Firestore]
                                                                                    │
                                                                          (real-time sync)
                                                                                    │
                                                                                    ▼
[Caregiver Web View] <──reads dashboard/report data── [FastAPI Backend] <──reads── [Firestore]
        │
        └──sets difficulty, language, reminders, patient profile (writes back to Firestore via FastAPI)
```

- **Firestore collections:** `patients/{id}/sessions`, `patients/{id}/reminders`, `patients/{id}/settings`, `patients/{id}/profile`
- **Data collected (minimal by design):** session scores/accuracy per domain, response time, session frequency, reminder completion, language preference, caregiver-provided personalization facts. No biometric or diagnostic data.

---

## 3. User Flows

### Caregiver = Controller
The caregiver holds administrative control of the application:
- Sets up patient profile (name, regional language, personalization facts for future LLM content)
- Sets game difficulty level manually
- Configures medicine/hydration/activity reminders
- Views daily engagement summary (streaks, trend)
- Reviews/downloads the AI-generated performance report (Phase 2)
- Adjusts settings anytime

### Patient = Player
The patient has a simplified, voice-guided experience with no administrative controls:
- Opens app → large-icon home screen with voice greeting
- Chooses a game (voice-prompted, in their own language)
- Plays session at the difficulty level the caregiver has set
- Receives reminder pop-ups during use
- Session ends → results sync live to caregiver's dashboard

---

## 4. AI/ML Components — Final Set

1. **Cognitive Performance Report (Phase 2)** — scikit-learn classifier on session data (synthetic-trained) → trend classification per domain → doctor-reviewable report (addresses NER's neurological specialist shortage by making rare consultations more effective)
2. **Personalized Memory Content (Phase 2)** — LLM-generated game questions from caregiver-submitted family facts → reinforces the core "generic tools fail because they're impersonal" thesis
3. **Manual difficulty control (Phase 1)** — caregiver-set, no algorithm required yet; autonomous/adaptive difficulty is a explicitly-flagged future enhancement, not a Phase 1 build item

---

## 5. Role Division — 6-Person Team

| # | Role | Responsibilities |
|---|---|---|
| 1 | Patient Frontend | Patient play view: game UI, voice-guided navigation, large-UI/accessibility compliance, session flow |
| 2 | Caregiver Frontend | Caregiver control panel: patient setup, difficulty settings, reminders config, dashboard (streaks/trend), report view |
| 3 | Backend + Firebase Integration | FastAPI endpoints, Firestore schema and real-time sync, Firebase Auth, hosting/deployment |
| 4 | Voice + Regional Language Content | Recording/sourcing regional-language audio prompts, i18n JSON config structure, Web Speech API fallback integration *(Varun's focus area)* |
| 5 | ML — Performance Report | Synthetic data generation, scikit-learn model for trend classification, report template/export (Phase 2, can start synthetic-data work early) |
| 6 *(if available)* | Pitch & Demo | Pitch deck, demo script, before/after comparison mock, LLM personalization feature (can double up once core build stabilizes) |

**Suggested sequencing:** Roles 1–4 focus entirely on Phase 1 (core MVP) first — get patient play flow + caregiver control panel + real-time sync working end-to-end before touching ML. Role 5 can build/validate the ML report in parallel using synthetic data, so it's ready to plug in once Phase 1 is stable. Role 6 starts pitch material early and folds in the LLM personalization feature only if time remains.

---

## 6. Build Priority Checklist

- [ ] Firestore schema (patients/sessions/reminders/settings/profile)
- [ ] FastAPI endpoints for session write/read, settings, reminders
- [ ] Patient play view: 1 game (memory recall) fully working end-to-end
- [ ] Caregiver control panel: difficulty setting + reminder config
- [ ] Caregiver dashboard: live-updating streak/trend view
- [ ] Regional language audio prompts + i18n config for 1 language
- [ ] Second game (pattern/object recognition) — only after first game + full loop works
- [ ] ML performance report (Phase 2)
- [ ] LLM personalized content (Phase 2)
