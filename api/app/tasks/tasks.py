from celery import Celery
from app.core.config import settings
import httpx
import logging

celery_app = Celery("tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@celery_app.task
def process_security_event(event_id: str):
    logging.info(f"Processing event: {event_id}")
    # Call Go engine for correlation
    try:
        with httpx.Client() as client:
            response = client.post(
                f"{settings.ENGINE_URL}/correlate",
                json={"event_id": event_id},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logging.error(f"Error calling engine: {e}")
        return {"status": "error", "message": str(e)}

@celery_app.task
def generate_report(threat_id: str):
    # Logic for generating PDF report
    pass
