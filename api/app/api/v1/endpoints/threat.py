from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.threat import ThreatDecision
from app.schemas.threat import ThreatDecisionRead
from app.api.deps import get_current_active_user
from app.models.user import User
from uuid import UUID

from fastapi.responses import StreamingResponse
from app.services import report_service
from io import BytesIO

router = APIRouter()

@router.get("/{threat_id}/report", response_class=StreamingResponse)
def get_threat_report(
    threat_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate a PDF report for a threat decision.
    """
    threat = db.query(ThreatDecision).filter(ThreatDecision.id == threat_id).first()
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    
    report_buffer = report_service.generate_threat_report(threat)
    return StreamingResponse(
        report_buffer, 
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=report_{threat_id}.pdf"}
    )

@router.get("/", response_model=List[ThreatDecisionRead])
def read_threats(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve threat decisions.
    """
    threats = db.query(ThreatDecision).offset(skip).limit(limit).all()
    return threats

@router.get("/{threat_id}", response_model=ThreatDecisionRead)
def read_threat(
    threat_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get threat decision by ID.
    """
    threat = db.query(ThreatDecision).filter(ThreatDecision.id == threat_id).first()
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat
