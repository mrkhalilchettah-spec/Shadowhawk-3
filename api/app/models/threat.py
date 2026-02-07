from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db import Base
import datetime

class ThreatDecision(Base):
    __tablename__ = "threat_decisions"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    risk_score = Column(Float, nullable=False)
    status = Column(String, default="open")
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class ThreatEvidence(Base):
    __tablename__ = "threat_evidence"
    decision_id = Column(UUID(as_uuid=True), ForeignKey("threat_decisions.id"), primary_key=True)
    signal_id = Column(UUID(as_uuid=True), ForeignKey("normalized_signals.id"), primary_key=True)
