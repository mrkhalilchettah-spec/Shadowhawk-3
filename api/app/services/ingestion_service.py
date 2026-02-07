from sqlalchemy.orm import Session
from app.models.event import SecurityEvent
from app.schemas.event import SecurityEventCreate
from app.tasks.tasks import process_security_event
import uuid

def create_event(db: Session, *, obj_in: SecurityEventCreate) -> SecurityEvent:
    db_obj = SecurityEvent(
        id=uuid.uuid4(),
        source=obj_in.source,
        event_type=obj_in.event_type,
        raw_data=obj_in.raw_data
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def process_event_async(event_id: uuid.UUID):
    process_security_event.delay(str(event_id))
