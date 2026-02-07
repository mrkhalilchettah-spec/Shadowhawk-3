-- Initial Schema for Shadowhawk Core

-- RBAC Tables
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Ingestion & Normalization
CREATE TABLE IF NOT EXISTS security_events (
    id UUID PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    raw_data JSONB NOT NULL,
    received_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS normalized_signals (
    id UUID PRIMARY KEY,
    event_id UUID REFERENCES security_events(id),
    signal_type VARCHAR(100) NOT NULL,
    entity_id VARCHAR(255) NOT NULL, -- IP, Domain, User, etc.
    entity_type VARCHAR(50) NOT NULL,
    confidence FLOAT DEFAULT 1.0,
    severity FLOAT DEFAULT 0.0,
    metadata JSONB,
    occurred_at TIMESTAMP WITH TIME ZONE NOT NULL,
    normalized_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Correlation Graph
CREATE TABLE IF NOT EXISTS graph_nodes (
    id VARCHAR(255) PRIMARY KEY,
    node_type VARCHAR(50) NOT NULL,
    properties JSONB,
    first_seen TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS graph_edges (
    id SERIAL PRIMARY KEY,
    source_node_id VARCHAR(255) REFERENCES graph_nodes(id),
    target_node_id VARCHAR(255) REFERENCES graph_nodes(id),
    edge_type VARCHAR(50) NOT NULL,
    weight FLOAT DEFAULT 1.0,
    properties JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_node_id, target_node_id, edge_type)
);

-- MITRE ATT&CK Mappings
CREATE TABLE IF NOT EXISTS mitre_techniques (
    id VARCHAR(20) PRIMARY KEY, -- e.g., T1059
    name VARCHAR(255) NOT NULL,
    tactic VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS signal_mitre_mapping (
    signal_id UUID REFERENCES normalized_signals(id),
    technique_id VARCHAR(20) REFERENCES mitre_techniques(id),
    confidence FLOAT DEFAULT 1.0,
    PRIMARY KEY (signal_id, technique_id)
);

-- Risk Scoring & Decisions
CREATE TABLE IF NOT EXISTS threat_decisions (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    risk_score FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT 'open', -- open, investigated, closed, false_positive
    assigned_to INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS threat_evidence (
    decision_id UUID REFERENCES threat_decisions(id),
    signal_id UUID REFERENCES normalized_signals(id),
    PRIMARY KEY (decision_id, signal_id)
);

-- Audit Logging (Append-only)
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(255),
    details JSONB,
    ip_address VARCHAR(45),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indices
CREATE INDEX idx_normalized_signals_entity ON normalized_signals(entity_id, entity_type);
CREATE INDEX idx_security_events_type ON security_events(event_type);
CREATE INDEX idx_graph_edges_source ON graph_edges(source_node_id);
CREATE INDEX idx_graph_edges_target ON graph_edges(target_node_id);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
