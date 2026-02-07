from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base
import datetime

class NormalizedSignal(Base):
    __tablename__ = "normalized_signals"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("security_events.id"))
    signal_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    confidence = Column(Float, default=1.0)
    severity = Column(Float, default=0.0)
    metadata = Column(JSON)
    occurred_at = Column(DateTime, nullable=False)
    normalized_at = Column(DateTime, default=datetime.datetime.utcnow)
