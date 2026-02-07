from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base
import datetime

class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    source = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    raw_data = Column(JSON, nullable=False)
    received_at = Column(DateTime, default=datetime.datetime.utcnow)
