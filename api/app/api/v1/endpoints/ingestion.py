from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.event import SecurityEventCreate
from app.services import ingestion_service
from app.api.deps import get_current_active_user
from app.models.user import User
import uuid

router = APIRouter()

@router.post("/", response_model=dict)
async def ingest_event(
    *,
    db: Session = Depends(get_db),
    event_in: SecurityEventCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Ingest a new security event.
    """
    event = ingestion_service.create_event(db, obj_in=event_in)
    # Background task to normalize and correlate
    ingestion_service.process_event_async(event.id)
    return {"id": event.id, "status": "accepted"}
