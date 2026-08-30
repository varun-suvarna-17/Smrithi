from typing import Optional
from pydantic import BaseModel, Field


class VoiceSynthesisRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to synthesize to speech")
    language: str = Field("as", description="Language code e.g. as, bn, hi, en, mni")
    speed_rate: Optional[float] = Field(1.0, ge=0.5, le=2.0, description="Speech rate multiplier")


class VoiceSynthesisResponse(BaseModel):
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    format: str = "mp3"
    duration_estimate_seconds: float
    language_used: str
    fallback_used: bool
    status: str
    message: str
