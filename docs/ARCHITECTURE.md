# Shadowhawk Core Architecture

## Data Flow
1. **Ingestion**: External systems send security events via JSON to the `/api/v1/ingest/` endpoint.
2. **Persistence**: Events are saved to the `security_events` table in PostgreSQL.
3. **Asynchronous Processing**: A Celery task is triggered to process the event.
4. **Correlation**: The Celery task calls the Go Engine's `/correlate` endpoint.
5. **Graph Analysis**: The Go Engine fetches normalized signals, updates the entity graph, and runs correlation rules.
6. **Risk Scoring**: The system calculates a risk score based on impact, exposure, and confidence.
7. **Threat Decision**: If a threat is detected, a `threat_decision` is created.
8. **Reporting**: Analysts can request a PDF report for any threat decision.

## Component Breakdown

### Go Correlation Engine
- **Graph Package**: Manages nodes (IPs, Domains, Users) and edges (Relationships).
- **Correlator Package**: Implements rules like "Suspicious Login -> Lateral Movement".
- **MITRE Mapper**: Maps detected patterns to MITRE ATT&CK techniques.

### Python API Layer
- **FastAPI**: Provides a high-performance RESTful interface.
- **SQLAlchemy**: ORM for database interactions.
- **Pydantic**: Data validation and schema enforcement.
- **Celery**: Background job processing.

### Storage & Cache
- **PostgreSQL**: Stores relational data with indices for fast lookups.
- **Redis**: Used as a Celery broker and for caching frequently accessed data.

## Security Design
- **JWT + RBAC**: Secure authentication and role-based access control.
- **Audit Logs**: Every mutation is logged in an append-only table.
- **Secure Defaults**: Environment-based configuration with no hardcoded secrets.
