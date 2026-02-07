from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class ThreatDecisionBase(BaseModel):
    title: str
    description: Optional[str] = None
    risk_score: float
    status: str = "open"

class ThreatDecisionRead(ThreatDecisionBase):
    id: UUID
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
