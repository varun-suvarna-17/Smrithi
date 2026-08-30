from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


class SessionCreate(BaseModel):
    gameType: Literal["memory_recall", "pattern_recognition"]
    startedAt: datetime
    endedAt: Optional[datetime] = None
    completed: bool
    languageUsed: str
    difficultyLevel: int          # integer, e.g. 1-3; rule computed by game engine
    correctCount: int
    wrongCount: int
    difficultyDropped: bool       # true if rule-based logic (3 wrong → easier) fired


class SessionOut(SessionCreate):
    sessionId: str
    createdAt: Optional[datetime] = None