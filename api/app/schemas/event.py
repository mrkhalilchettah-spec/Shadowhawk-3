from pydantic import BaseModel
from typing import Dict, Any, Optional
from uuid import UUID

class SecurityEventBase(BaseModel):
    source: str
    event_type: str
    raw_data: Dict[str, Any]

class SecurityEventCreate(SecurityEventBase):
    pass

class SecurityEvent(SecurityEventBase):
    id: UUID
    
    class Config:
        from_attributes = True
