# Shadowhawk Core

Shadowhawk Core is a military-grade, on-prem Autonomous Cyber Intelligence Engine. It is designed to ingest security signals, normalize them, correlate them using graph-based logic, and produce actionable threat decisions.

## Architecture

- **Go Correlation Engine**: High-performance graph-based correlation and MITRE ATT&CK mapping.
- **Python FastAPI API**: Robust orchestration layer for ingestion, risk scoring, and reporting.
- **PostgreSQL**: Reliable persistent storage for events, signals, and threats.
- **Redis**: Fast caching and task queue management.
- **Celery**: Asynchronous tasks for heavy processing and report generation.
- **Docker**: Simplified deployment via a single-container multi-stage build (or docker-compose).

## Quick Start

### Prerequisites
- Docker and Docker Compose

### Deployment
1. Clone the repository.
2. Copy `.env.example` to `.env` and configure your settings.
3. Run `docker-compose up -d`.

The API will be available at `http://localhost:8000` and the engine at `http://localhost:8080`.

## Features
- **Engine-first design**: Deterministic correlation logic.
- **MITRE ATT&CK Integration**: Automatic mapping of threats to the MITRE framework.
- **Confidence-aware Risk Scoring**: Multi-factor risk calculation.
- **Professional PDF Reports**: Executive and technical reporting.
- **Immutable Audit Logging**: Append-only logs for compliance and forensics.

## API Documentation
Once running, visit `http://localhost:8000/docs` for interactive Swagger UI documentation.
