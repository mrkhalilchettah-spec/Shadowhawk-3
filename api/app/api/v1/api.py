from fastapi import APIRouter
from app.api.v1.endpoints import ingestion, threat, auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(ingestion.router, prefix="/ingest", tags=["ingestion"])
api_router.include_router(threat.router, prefix="/threats", tags=["threats"])
