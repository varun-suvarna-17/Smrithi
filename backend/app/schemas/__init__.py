from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# ----------------- Enum Definitions -----------------

class UserRole(str, Enum):
    PATIENT = "patient"
    CAREGIVER = "caregiver"
    DOCTOR = "doctor"
    ADMIN = "admin"

class DementiaStage(str, Enum):
    MCI = "Mild Cognitive Impairment (MCI)"
    EARLY = "Early Stage"
    MODERATE = "Moderate Stage"
    ADVANCED = "Advanced Stage"
    UNKNOWN = "Not Diagnosed / Undetermined"

class CognitiveGameType(str, Enum):
    MEMORY = "memory"
    ATTENTION = "attention"
    SEQUENCE = "sequence"
    PATTERN = "pattern"
    RECOGNITION = "recognition"

class CognitiveDomain(str, Enum):
    MEMORY = "Memory"
    ATTENTION = "Attention"
    REASONING_SEQUENCE = "Reasoning & Sequence"
    PATTERN_RECOGNITION = "Pattern Recognition"
    VISUAL_RECOGNITION = "Visual & Cultural Recognition"

class ReminderType(str, Enum):
    MEDICATION = "medication"
    COGNITIVE_GAME = "cognitive_game"
    HYDRATION = "hydration"
    DAILY_ROUTINE = "daily_routine"
    DOCTOR_VISIT = "doctor_visit"

class AdaptiveAction(str, Enum):
    INCREASE = "increase"
    MAINTAIN = "maintain"
    DECREASE = "decrease"

# ----------------- Auth Schemas -----------------

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str
    role: UserRole = UserRole.CAREGIVER
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    role: UserRole
    full_name: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: UserRole
    phone: Optional[str] = None
    created_at: Optional[str] = None

# ----------------- Patient Schemas -----------------

class PatientCreate(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=40, le=120)
    gender: Optional[str] = "Other"
    dementia_stage: DementiaStage = DementiaStage.EARLY
    preferred_language: str = Field("as", description="NER language code e.g. as, bn, mni, brx, lus, kha, grt, en, hi")
    emergency_contact: Optional[str] = None
    medical_notes: Optional[str] = None
    baseline_mmse_score: Optional[int] = Field(None, ge=0, le=30, description="Mini-Mental State Exam baseline (0-30)")
    caregiver_id: Optional[str] = None

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=40, le=120)
    gender: Optional[str] = None
    dementia_stage: Optional[DementiaStage] = None
    preferred_language: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_notes: Optional[str] = None
    baseline_mmse_score: Optional[int] = Field(None, ge=0, le=30)
    caregiver_id: Optional[str] = None
    current_difficulty_levels: Optional[Dict[str, int]] = None

class PatientResponse(BaseModel):
    id: str
    name: str
    age: int
    gender: Optional[str] = "Other"
    dementia_stage: str
    preferred_language: str
    emergency_contact: Optional[str] = None
    medical_notes: Optional[str] = None
    baseline_mmse_score: Optional[int] = None
    caregiver_id: Optional[str] = None
    current_difficulty_levels: Dict[str, int] = Field(default_factory=lambda: {
        "memory": 1, "attention": 1, "sequence": 1, "pattern": 1, "recognition": 1
    })
    total_sessions_completed: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

# ----------------- Caregiver Schemas -----------------

class CaregiverCreate(BaseModel):
    name: str = Field(..., min_length=2)
    relationship: str = Field("Family Caregiver", description="Relationship to patient e.g. Daughter, Son, Nurse, Spouse")
    phone: str
    email: EmailStr
    user_id: Optional[str] = None

class CaregiverUpdate(BaseModel):
    name: Optional[str] = None
    relationship: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class CaregiverPatientLink(BaseModel):
    patient_id: str
    caregiver_id: str

class CaregiverResponse(BaseModel):
    id: str
    name: str
    relationship: str
    phone: str
    email: str
    user_id: Optional[str] = None
    assigned_patients: List[str] = Field(default_factory=list)
    created_at: Optional[str] = None

# ----------------- Game Schemas -----------------

class GameInfo(BaseModel):
    id: str
    name: str
    cognitive_domain: CognitiveDomain
    description: str
    supported_difficulty_range: List[int] = [1, 2, 3, 4, 5]
    ner_cultural_context: str

class StartGameRequest(BaseModel):
    patient_id: str
    game_type: CognitiveGameType
    difficulty_level: Optional[int] = Field(None, ge=1, le=5, description="If omitted, patient's current adaptive level is used")
    language: Optional[str] = Field(None, description="If omitted, patient's preferred language is used")

class StartGameResponse(BaseModel):
    session_id: str
    patient_id: str
    game_type: CognitiveGameType
    game_name: str
    cognitive_domain: str
    difficulty_level: int
    language: str
    instructions: str
    total_rounds: int
    rounds_data: List[Dict[str, Any]]
    created_at: str

class GameAttemptCreate(BaseModel):
    patient_id: str
    session_id: Optional[str] = None
    game_type: CognitiveGameType
    difficulty_level: int = Field(..., ge=1, le=5)
    score: int = Field(..., ge=0)
    total_questions: int = Field(..., ge=1)
    correct_answers: int = Field(..., ge=0)
    response_time_ms: int = Field(..., ge=0, description="Total or average response latency in milliseconds")
    mistakes: int = Field(0, ge=0)
    attempts: int = Field(1, ge=1)
    session_duration_seconds: Optional[int] = Field(0, ge=0)
    details: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

class GameAttemptResponse(BaseModel):
    id: str
    patient_id: str
    session_id: Optional[str] = None
    game_type: str
    cognitive_domain: str
    difficulty_level: int
    score: int
    total_questions: int
    correct_answers: int
    accuracy: float
    response_time_ms: int
    mistakes: int
    attempts: int
    session_duration_seconds: int
    timestamp: str
    next_recommended_difficulty: int
    adaptive_recommendation: str

# ----------------- Adaptive Difficulty Schemas -----------------

class AdaptiveEvaluationRequest(BaseModel):
    patient_id: str
    game_type: CognitiveGameType
    current_difficulty: Optional[int] = Field(None, ge=1, le=5)

class AdaptiveMetricsAnalyzed(BaseModel):
    rolling_accuracy: float
    average_response_time_ms: float
    mistake_rate: float
    performance_streak: int
    trend_slope: float
    recent_attempts_count: int

class AdaptiveEvaluationResponse(BaseModel):
    patient_id: str
    game_type: CognitiveGameType
    current_difficulty: int
    recommended_difficulty: int
    action: AdaptiveAction
    confidence_score: float
    metrics: AdaptiveMetricsAnalyzed
    rationale: str
    evaluated_at: str

# ----------------- Progress & Analytics Schemas -----------------

class DomainScore(BaseModel):
    domain_name: str
    game_type: str
    total_sessions: int
    average_accuracy: float
    average_response_time_ms: float
    current_difficulty_level: int
    status: str  # "improving", "stable", "needs_attention"
    recent_trend_slope: float

class PatientAnalyticsResponse(BaseModel):
    patient_id: str
    patient_name: str
    dementia_stage: str
    total_games_played: int
    total_play_time_minutes: float
    overall_accuracy_percentage: float
    overall_avg_response_time_ms: float
    domain_breakdown: Dict[str, DomainScore]
    accuracy_history: List[Dict[str, Any]]
    response_time_history: List[Dict[str, Any]]
    difficulty_progression: Dict[str, List[Dict[str, Any]]]
    improvement_indicators: Dict[str, Any]
    generated_at: str

# ----------------- Language & Multilingual Schemas -----------------

class LanguageInfo(BaseModel):
    code: str
    name: str
    native_name: str
    script: str
    region: str
    tts_supported: bool

class TranslationRequest(BaseModel):
    text: str
    source_language: str = "en"
    target_language: str

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    service_used: str

class LocalizedContentResponse(BaseModel):
    language: str
    language_name: str
    common_prompts: Dict[str, str]
    game_vocabulary: Dict[str, Dict[str, str]]

# ----------------- Voice / TTS Schemas -----------------

class VoiceSynthesisRequest(BaseModel):
    text: str = Field(..., min_length=1)
    language: str = Field("as", description="Language code e.g. as, bn, hi, en, mni")
    speed_rate: Optional[float] = Field(1.0, ge=0.5, le=2.0)

class VoiceSynthesisResponse(BaseModel):
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    format: str = "mp3"
    duration_estimate_seconds: float
    language_used: str
    fallback_used: bool
    status: str
    message: str

# ----------------- Reminder Schemas -----------------

class ReminderCreate(BaseModel):
    patient_id: str
    title: str
    message: str
    reminder_type: ReminderType = ReminderType.COGNITIVE_GAME
    scheduled_time: str = Field(..., description="ISO 8601 string e.g. 2026-08-29T18:00:00")
    recurring: bool = False
    frequency: Optional[str] = Field("daily", description="daily, weekly, custom")
    caregiver_id: Optional[str] = None

class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    reminder_type: Optional[ReminderType] = None
    scheduled_time: Optional[str] = None
    recurring: Optional[bool] = None
    frequency: Optional[str] = None
    is_completed: Optional[bool] = None

class ReminderResponse(BaseModel):
    id: str
    patient_id: str
    title: str
    message: str
    reminder_type: str
    scheduled_time: str
    recurring: bool
    frequency: Optional[str] = None
    is_completed: bool
    caregiver_id: Optional[str] = None
    created_at: str

# ----------------- Alert Schemas -----------------

class AlertItem(BaseModel):
    id: str
    patient_id: str
    caregiver_id: Optional[str] = None
    alert_type: str  # "performance_drop", "inactivity", "high_latency", "streak_milestone"
    severity: str    # "info", "warning", "critical"
    message: str
    created_at: str
    is_read: bool = False

# ----------------- AI / Progress Report Schemas -----------------

class ProgressReportResponse(BaseModel):
    report_id: str
    patient_id: str
    patient_name: str
    dementia_stage: str
    reporting_period: str
    total_sessions_analyzed: int
    cognitive_domains: Dict[str, Dict[str, Any]]
    clinical_summary: str
    observed_strengths: List[str]
    areas_to_watch: List[str]
    performance_trend: str
    adherence_and_consistency: Dict[str, Any]
    caregiver_actionable_suggestions: List[str]
    recent_activity: List[Dict[str, Any]]
    is_ai_generated: bool
    ai_engine: str
    disclaimer: str = "This progress-assistance report is generated for caregivers and healthcare facilitators to monitor cognitive engagement. It is NOT a medical diagnosis or replacement for clinical neuropsychological assessment."
    created_at: str
