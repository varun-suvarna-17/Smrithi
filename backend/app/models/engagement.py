from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EngagementSummary(BaseModel):
    """
    Mirrors the engagementSummary/current Firestore document.
    Never written directly by clients — always recomputed by FastAPI.
    """
    streakCount: int               # consecutive days with >= 1 completed session
    weeklySessionCount: int        # sessions in trailing 7 days
    reminderAdherenceRate: float   # 0.0-1.0, trailing 7 days
    lastSessionAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

