from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


class ReminderCreate(BaseModel):
    type: Literal["medicine", "activity"]
    title: str
    scheduledTime: str            # HH:mm local time
    recurrence: Literal["daily", "once"]


class ReminderStatusUpdate(BaseModel):
    status: Literal["pending", "completed", "missed"]


class ReminderOut(BaseModel):
    reminderId: str
    type: str
    title: str
    scheduledTime: str
    recurrence: str
    status: str
    lastTriggeredAt: Optional[datetime] = None
    createdAt: Optional[datetime] = None