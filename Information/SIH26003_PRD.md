# SPARSH
### AI-Based Cognitive Gaming & Memory Assistance Platform for Elderly Dementia Patients in the North Eastern Region

**Product Requirements Document**
Smart India Hackathon 2026 | Problem Statement SIH26003

---

## 1. Problem Statement

> **Refined Problem Statement:**
> Elderly dementia patients and their caregivers in the North Eastern Region need a way to engage in cognitive therapy in their own language and cultural context, because existing digital cognitive-gaming tools are built around generic/Western content — leading to poor engagement, patient confusion, and caregivers falling back to no digital support at all — compounded by limited specialist access and low connectivity in the region.

Personnel serving the elderly population of the North Eastern Region (NER) face a compounding set of barriers: rising rates of age-related cognitive decline, some of the country's most severe neurological specialist shortages, and a complete absence of digital cognitive-care tools adapted to the region's languages and cultural context. The result is a population whose caregivers are largely left to manage dementia progression alone, with no structured, accessible, or culturally relevant support.

---

## 2. Target Users — Dual-User Design

The product is designed around two users of equal weight, since a dementia-care tool only succeeds if it works for both the patient using it and the caregiver relying on it.

### Persona 1: The Patient
- Elderly individual (60+), based in a rural or semi-urban part of the North Eastern Region
- Early-to-moderate stage dementia — experiencing memory decline, confusion, anxiety, and social isolation
- Comfortable primarily in a regional or tribal language; low digital literacy and limited smartphone familiarity
- Needs simple, non-intimidating interaction and content that feels familiar rather than clinical or foreign

### Persona 2: The Caregiver
- A family member living with or near the patient (not a healthcare/ASHA worker — MVP is scoped to a single-patient, home view)
- Not medically trained; juggling caregiving alongside other household and work responsibilities
- Currently has no structured way to track whether the patient's cognitive state is stable, improving, or declining — relies on gut feel and occasional clinic visits
- Needs a low-effort way to monitor engagement/progress and wants reminders handled automatically rather than manually tracked

---

## 3. Market & User Research

Framed using both qualitative signal (the "why") and quantitative scale (the "how much") to justify the problem beyond assumption.

### 3.1 Quantitative Scale — Proving How Many
- National estimates put dementia prevalence at 7.4% among Indians aged 60+, with roughly 8.8 million people affected — and the burden varies significantly by state and by the urban/rural divide.
- Neurological specialist access in NER is a documented crisis: large parts of Arunachal Pradesh, Manipur, Nagaland, and Tripura have no full-time neurosurgeon at all, and Mizoram has none whatsoever. Most districts depend on visiting consultants, and patients face critical delays during emergencies.
- NER's remoteness compounds the access problem: in tribal-majority NER states such as Nagaland — where 61% of people are multidimensionally poor — many rural and remote zones still lack basic transport connectivity, which markedly affects timely access to care.
- An Indian home-care study of dementia patients found moderate-to-severe caregiver burden scores, alongside significant gaps in home-based care knowledge and caregiving practices — with rural participants showing markedly different awareness levels than urban ones.

### 3.2 Qualitative Hook — Proving Why It Hurts
- A scoping review of Indian dementia caregivers found that caregiving experiences in India are shaped by cultural and socioeconomic context in ways that remain understudied compared to Western-focused literature, with rural caregivers facing distinct gaps in home-based support.
- A participatory study testing conversational robots for Indian dementia care had to exclude non-English speakers entirely — the study only included participants able to engage verbally in English with the robot.
- Popular global dementia apps (e.g. Lumosity, AmuseIT) are built around English-language quizzes and Western cultural references, engaging patients through quiz questions and visuals designed to spark conversation and tap into past memories — but none of this content is adapted for NER's tribal or vernacular contexts.

> **The Pitch Hook:**
> Even the researchers studying dementia technology in India had to exclude non-English speakers from their own study — the exact population NER's elderly patients belong to.

---

## 4. MVP Scope

Cut ruthlessly from the full 8-part "Expected Solution" in the original problem statement. Every inclusion or exclusion below is tied directly to the personas and research above — not to build convenience.

### 4.1 In Scope — Core MVP

| Component | Why It's In |
|---|---|
| 2 adaptive cognitive games (memory recall + pattern/object recognition) | Covers the two most impactful cognitive domains without spreading thin across all listed game types |
| Regional language + voice-assisted interaction (1 NER language for demo, e.g. Assamese or Khasi) | This is the core differentiator and pitch hook — cutting this defeats the PRD's central thesis |
| Culturally familiar visuals & audio (local imagery, folk motifs, familiar sounds) | Directly answers the "existing tools aren't culturally relevant" insight; cheap to build (asset swap), high pitch impact |
| Caregiver dashboard — single patient view | Shows game completion, streaks, and a simple engagement trend — matches the locked-in home-caregiver persona |
| Medicine / activity reminders (scheduled notifications) | Low build effort, high perceived value, explicitly listed in the PS |
| Simple, elderly-friendly UI (large text/buttons, minimal navigation) | Non-negotiable — without this the product is unusable by its own target persona |

### 4.2 Out of Scope — Deferred to Future Scope

| Component | Why It's Cut |
|---|---|
| Full adaptive difficulty via ML | Real adaptive ML needs usage data unavailable in a hackathon. MVP substitutes rule-based logic (e.g. 3 wrong answers → easier level) as an explicit placeholder for a future model |
| Multi-language support beyond 1 demo language | NER has dozens of languages/dialects — supporting even 3–4 well is a localization project, not a hackathon feature |
| Offline sync / low-connectivity mode | Real offline-first architecture (conflict resolution, local sync) is a substantial engineering lift; stated as a designed-for constraint, not built |
| Full behavioral analytics dashboard | Overkill for a family caregiver; replaced with a simple 3-metric view |
| Production-grade secure data management | Approach (data minimization, local-storage-first) is stated in the technical section; not implemented at production compliance level in the MVP |
| Medical appointment reminders | Cut for time; daily medicine/hydration reminders already demonstrate the capability |

> **One-Line MVP Pitch:**
> A cognitive gaming app for elderly dementia patients in NER, in their own language and cultural context, with a simple caregiver view — because even research-grade dementia tech in India excludes non-English speakers.

---

## 5. Key Technical Challenges & MVP Response

Each challenge below is answered honestly — including where the MVP intentionally punts and why — since this is exactly what judges probe on.

| Challenge | Real Risk | MVP's Answer |
|---|---|---|
| Regional language/dialect coverage | NER has dozens of languages; demoing in one risks looking like a token gesture | Content-layer abstraction: games/UI are language-agnostic, only text/audio assets swap per language. Demo 1 language; show config proving it's swap-in-ready for others |
| Adaptive difficulty without real usage data | Claiming ML-driven adaptation with no training data is a credibility risk | Rule-based adaptive logic as an explicit placeholder for a future ML model — framed as engineering for adaptability, not fake ML |
| Elderly usability (low digital literacy) | Complex navigation/icons/gestures alienate the exact target user | Large tap targets, voice-first navigation, single-screen game flow, no nested menus |
| Low-connectivity / offline access | Real offline sync isn't buildable in a hackathon | State target architecture (local-first storage, sync-on-connectivity) as a design decision; don't demo what isn't built |
| Caregiver trust & alert overload | A dashboard full of clinical metrics adds burden instead of relief | Deliberately minimal dashboard — 3 metrics max, no jargon, no false urgency |
| Data sensitivity (health + elderly PII) | Real compliance requirements judges will probe on | Local-storage-first, minimal-collection approach — data stays on-device by default in the MVP |
| Engagement/retention over time | Cognitive games are often abandoned once novelty fades | Cultural relevance (familiar visuals/language) is the retention lever — generic tools fail because they don't feel familiar enough to stay engaging |

---

## 6. Success Metrics

Split deliberately into long-term product metrics and what can honestly be demonstrated at judging — conflating the two is a common hackathon pitch mistake.

### 6.1 Long-Term Product Success Metrics

| Metric | What It Proves |
|---|---|
| Weekly active engagement rate (≥1 session/week) | Retention — the real failure mode surfaced in caregiver research |
| Caregiver-reported perceived cognitive stability/improvement | Whether the tool feels useful to the person who'd actually keep using it |
| Reminder adherence rate | Whether the tool reduces caregiver mental load, not just adds a screen to check |
| % of sessions completed in regional language vs. default | Validates the core cultural-relevance thesis |
| Caregiver dashboard check-in frequency | Proxy for whether caregivers trust and rely on it, versus ignoring it |

### 6.2 Hackathon Demo Metrics
- Live demo: patient completes a game session in regional language → caregiver dashboard updates in real time (streak + reminder status)
- Show the language-swap architecture (config-driven asset loading) to prove scalability beyond the one demo language
- Show the rule-based difficulty adjustment triggering live (e.g. force 3 wrong answers, watch difficulty drop)
- If time permits: a side-by-side "before/after" — generic English cognitive game vs. the culturally-adapted version — to make the differentiation immediately visible to judges

> **Honesty Flag:**
> Do not claim "improved cognitive outcomes" as a hackathon success metric — there is no clinical trial behind it, and judges in health-tech categories will call this out quickly. Frame outcomes as hypothesized long-term impact; demo metrics as engagement/usability proof.

---

## 7. Future Scope

- Multi-language expansion across additional NER languages/dialects, built on the config-driven content layer
- True adaptive difficulty via an ML model trained on real usage data collected post-launch
- Offline-first architecture with local-to-cloud sync for genuinely low-connectivity areas
- Expansion of the caregiver role to include healthcare/ASHA workers with a multi-patient caseload view
- Production-grade encryption, compliance, and role-based access control for sensitive health data
- Clinical validation studies to substantiate cognitive-outcome claims
