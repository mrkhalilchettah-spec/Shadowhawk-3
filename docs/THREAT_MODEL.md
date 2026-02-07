# Shadowhawk Core Threat Model

## Asset Inventory
1. **Security Signals**: Normalized data from multiple sources.
2. **Correlation Logic**: Proprietary rules and graph structures.
3. **Audit Logs**: Record of all system activities.
4. **User Credentials**: Access to the system.

## Trust Boundaries
- **External Network -> API**: Incoming security events.
- **API -> Engine**: Internal communication for correlation.
- **Application -> Database/Redis**: Persistent storage and caching.

## Identified Threats & Mitigations

### 1. SQL Injection
- **Threat**: Attacker sends malicious SQL in JSON payloads.
- **Mitigation**: Use SQLAlchemy ORM and parameterized queries for all database interactions.

### 2. Unauthorized Access
- **Threat**: Attacker gains access to the API without credentials.
- **Mitigation**: Mandatory JWT authentication for all endpoints except health checks. Role-based access control (RBAC) to limit functionality.

### 3. Log Tampering
- **Threat**: Attacker modifies audit logs to hide their tracks.
- **Mitigation**: Use an append-only database design for audit logs. Database-level permissions to prevent updates/deletes on the audit table.

### 4. Denial of Service (DoS)
- **Threat**: Flooding the ingestion endpoint with massive amounts of data.
- **Mitigation**: Rate limiting at the API layer and asynchronous processing via Celery to prevent blocking the main thread.

### 5. Sensitive Data Exposure
- **Threat**: API keys or database credentials leaked in logs or code.
- **Mitigation**: Secrets managed via environment variables. Sensitive data filtered from logs.
