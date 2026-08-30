from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CaregiverCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    preferredDashboardLanguage: str = "en"


class CaregiverOut(BaseModel):
    caregiverId: str
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    preferredDashboardLanguage: str
    createdAt: Optional[datetime] = None

