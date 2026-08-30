from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PatientCreate(BaseModel):
    name: str
    age: int
    contentLanguage: str          # opaque string — validated by content team, not here
    avatarAssetId: Optional[str] = None


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    contentLanguage: Optional[str] = None
    avatarAssetId: Optional[str] = None


class PatientOut(BaseModel):
    patientId: str
    name: str
    age: int
    contentLanguage: str
    avatarAssetId: Optional[str] = None
    createdAt: Optional[datetime] = None