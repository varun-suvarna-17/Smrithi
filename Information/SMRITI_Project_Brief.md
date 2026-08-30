# Project Brief: SMRITI (SIH26003)
### AI-Based Cognitive Gaming & Memory Assistance Platform for Elderly Dementia Patients in the North Eastern Region (NER)

**Context:** This is a Smart India Hackathon 2026 (SIH) submission. SIH is India's national government-run hackathon (organized by AICTE/Ministry of Education's Innovation Cell). Teams pick an official problem statement (PS) released by a government ministry/department, submit an idea PPT + demo video for national screening, and if shortlisted, build a working prototype in a 36-hour Grand Finale.

---

## 1. Official Problem Statement (SIH26003)

The North Eastern Region (NER) of India is seeing rising rates of dementia and memory loss among the elderly, compounded by extremely limited access to specialized neurological/cognitive care due to remote geography and healthcare infrastructure gaps. Patients experience memory decline, confusion, anxiety, and social isolation; caregivers struggle with continuous monitoring and engagement. There is no affordable, culturally inclusive digital therapeutic solution for this population.

**Officially requested solution components:**
- Interactive cognitive games (memory, attention, daily-routine recall, pattern/object recognition)
- AI/ML-driven adaptive difficulty based on patient performance
- Multilingual, voice-assisted interaction in regional languages
- Culturally familiar visuals/sounds/themes
- Reminders (medicine, hydration, daily activities, appointments)
- Caregiver/healthcare-worker monitoring dashboard
- Offline functionality for low-connectivity areas
- Simple, elderly-friendly mobile/tablet UI

---

## 2. Refined Problem Statement (our framing)

> Elderly dementia patients and their caregivers in the North Eastern Region need a way to engage in cognitive therapy in their own language and cultural context, because existing digital cognitive-gaming tools are built around generic/Western content — leading to poor engagement, patient confusion, and caregivers falling back to no digital support at all — compounded by limited specialist access and low connectivity in the region.

**Core differentiator/thesis:** Existing dementia tech (even research studies conducted in India) defaults to English and generic Western content, excluding the exact population NER's elderly patients belong to. SMRITI's edge is genuine cultural/linguistic adaptation, not just translation.

---

## 3. Target Users (Dual-User Design)

**Patient:** Elderly (60+), rural/semi-urban NER, early-to-moderate dementia, low digital literacy, comfortable only in a regional/tribal language. Needs simple, non-intimidating, culturally familiar interaction.

**Caregiver:** A family member at home (NOT a healthcare/ASHA worker — MVP is single-patient, home-view only). Not medically trained, time-constrained, currently has no structured way to track the patient's cognitive trend. **The caregiver is the "controller"** of the application — sets game difficulty manually, configures reminders, views progress. The patient only plays; no admin controls on their side.

---

## 4. Supporting Research (used in the pitch)

- Dementia prevalence in India: 7.4% among adults 60+, ~8.8 million people (Lee et al., Alzheimer's & Dementia, 2023)
- NER has only 55 practising neurosurgeons across 8 states (0.35 per million, vs. India's national average of 1 per million); Mizoram has zero neurosurgeons (Outlook India, 2025, citing Neurology India correspondence)
- 90% gap in dementia diagnosis and care in India generally (Lima et al., Journal of Participatory Medicine, 2025)
- A 2025 participatory study testing conversational robots for dementia care in India had to address major gaps in speech recognition and cultural adaptation for the Indian context — underscoring that even research-grade tech underserves this population
- Popular global dementia apps (Lumosity, AmuseIT) are English/Western-content-only, with no NER-specific adaptation

**Pitch hook:** "Even research-grade dementia technology in India struggles with cultural and language adaptation — the exact population NER's elderly patients belong to."

---

## 5. MVP Scope

**In scope (build this):**
- 2 adaptive cognitive games: memory recall + pattern/object recognition
- Voice-assisted interaction in 1 NER language for demo (e.g. Assamese or Khasi), via pre-recorded audio prompts (not live speech-to-text — reliability risk for a live demo)
- Culturally familiar visuals/audio (local imagery, folk motifs)
- Caregiver dashboard: single-patient view, sets difficulty manually, views engagement streak/trend
- Medicine/activity reminders (scheduled notifications)
- Simple, elderly-friendly UI (large text/buttons, minimal navigation)
- **AI feature #1:** ML-generated cognitive performance report — a scikit-learn classifier (trained on synthetic session data) that classifies trend per cognitive domain (improving/stable/declining) and outputs a doctor-reviewable report, addressing the specialist-access gap
- **AI feature #2 (stretch):** LLM-personalized memory content — caregiver inputs family facts (names, hometown, festival, memory) once; an LLM generates custom memory-recall questions from them

**Explicitly out of scope for MVP (stated as future work):**
- Real adaptive/auto difficulty ML (caregiver controls it manually for now)
- Multi-language support beyond 1 demo language
- True offline-first sync (state it as designed-for architecture, don't build it)
- Full behavioral analytics dashboard (kept to 3 simple metrics instead)
- Production-grade security/compliance (state minimal-collection, local-storage-first approach instead)
- Medical appointment reminders (only medicine/hydration/activity reminders are built)
- Voice input / speech-to-text (flagged as a live-demo reliability risk)

---

## 6. Technical Stack

- **Frontend:** React + Vite, mobile-responsive web app (not native mobile)
- **Backend:** FastAPI (Python)
- **Database/Realtime sync:** Firebase (Firestore) + Firebase Auth — chosen specifically for real-time sync (patient session completion instantly reflects on caregiver dashboard)
- **Voice/language layer:** Pre-recorded regional-language audio + Web Speech API (TTS) as fallback; content stored in i18n JSON configs (`content/as.json`, `content/en.json`) — config-driven so new languages are just new files, not new code
- **ML:** scikit-learn (logistic regression or decision tree) trained on synthetic session data for the performance-trend classifier

**Backend folder structure (in progress):**
```
backend/app/
├── main.py
├── core/ (config.py, firebase_init.py)
├── models/ (patient.py, session.py, reminder.py — Pydantic schemas)
├── routes/ (profile.py, settings.py, sessions.py, reminders.py, report.py)
└── services/ (firestore_service.py, ml_service.py, voice_service.py)
```

**Firestore data model:** `patients/{id}/sessions`, `patients/{id}/reminders`, `patients/{id}/settings`, `patients/{id}/profile`. Data collected is deliberately minimal — session scores/accuracy per domain, response time, session frequency, reminder completion, language preference. No biometric or diagnostic data.

---

## 7. User Flows

**Patient flow:** Open app (voice greeting, large icons) → Choose a game (voice-prompted, own language) → Play session (difficulty set by caregiver) → Reminder pop-up during use → Session complete → syncs live to caregiver dashboard

**Caregiver flow:** Open dashboard (single-patient view) → See daily summary (streak, trend) → Check reminders (done/missed) → Get alert if engagement drops → Adjust settings (difficulty, reminder times)

---

## 8. Team Structure (6 people, backend-first sequencing)

Backend is built first; frontend implementation happens after, using designs prepared in parallel.

1. **DB/Auth/Firebase setup** — Firestore schema, Auth, FastAPI-Firebase integration
2. **Gaming logic** — game mechanics, scoring, session data, reminders logic
3. **ML training work** — synthetic data generation, scikit-learn model for the progress report
4. **Voice layer work** — regional-language audio, i18n config *(project owner's personal focus area)*
5. **Design lead** — patient game UI/UX + caregiver dashboard UI/UX + color theme, via Claude Design/Stitch — runs in parallel with backend, not after, so frontend implementation isn't blocked later
6. **Dedicated PPT/pitch lead** — narrative, slides, demo script — runs continuously from day one

Once backend stabilizes, roles 1 and 2 are expected to pivot into React frontend implementation using the Design Lead's finished mockups.

---

## 9. Success Metrics

**Long-term (vision):** weekly active engagement rate, caregiver-reported perceived stability/improvement, reminder adherence rate, % sessions in regional language vs. default, caregiver dashboard check-in frequency.

**Hackathon demo metrics:** live patient session → real-time caregiver dashboard update; language-swap config shown live; rule-based difficulty change triggered live; optional before/after comparison (generic vs. culturally-adapted game).

**Explicit honesty flag:** Do not claim "improved cognitive outcomes" — there's no clinical trial behind this. Outcomes are framed as hypothesized long-term impact; only engagement/usability is demoed as proof.

---

## 10. Current Status

PRD, technical spec, git repo, and backend boilerplate (FastAPI + Firebase) are in progress/complete. Pitch deck slides are being drafted and iteratively reviewed slide-by-slide for accuracy against the above scope (a recurring issue has been slides overclaiming auto-adaptive difficulty, which contradicts the caregiver-manual-control decision — worth double-checking any new content against this doc for that specific conflict).
