-- ==============================================================================
-- TECHCORP SI - Schéma Relationnel PostgreSQL
-- Date : Septembre 2026
-- Compatible PostgreSQL 16
-- ==============================================================================

-- 1. Référentiel des machines (Inventaire normalisé)
CREATE TABLE IF NOT EXISTS servers (
    hostname VARCHAR(64) PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,
    role VARCHAR(64) NOT NULL,
    os VARCHAR(64),
    environment VARCHAR(32) NOT NULL, -- PROD, DEV, STAGING, etc.
    inventory_status VARCHAR(32) NOT NULL, -- UP, DOWN, MAINTENANCE, etc.
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Services exposés par les serveurs
CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    hostname VARCHAR(64) REFERENCES servers(hostname) ON DELETE CASCADE,
    service_name VARCHAR(64) NOT NULL,
    port INTEGER NOT NULL,
    expected_state VARCHAR(32) NOT NULL DEFAULT 'UP',
    CONSTRAINT uq_server_service UNIQUE (hostname, service_name, port)
);

-- 3. Incidents et demandes d'exploitation (Tickets)
CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    hostname VARCHAR(64) REFERENCES servers(hostname) ON DELETE SET NULL,
    priority VARCHAR(32) NOT NULL, -- CRITICAL, HIGH, MEDIUM, LOW
    status VARCHAR(32) NOT NULL DEFAULT 'open', -- open, in_progress, resolved, closed
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

-- 4. Historique des contrôles de services et sondes TCP
CREATE TABLE IF NOT EXISTS service_checks (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hostname VARCHAR(64) REFERENCES servers(hostname) ON DELETE CASCADE,
    port INTEGER NOT NULL,
    tcp_result VARCHAR(32) NOT NULL, -- SUCCESS, FAILED, TIMEOUT
    latency_ms NUMERIC(8, 2),
    source VARCHAR(64) NOT NULL DEFAULT 'network_probe'
);

-- 5. Événements et journaux techniques parsés
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    level VARCHAR(16) NOT NULL, -- INFO, WARN, ERROR, CRITICAL
    hostname VARCHAR(64) REFERENCES servers(hostname) ON DELETE SET NULL,
    component VARCHAR(64),
    message TEXT NOT NULL
);

-- 6. Traçabilité et audit du nettoyage ETL
CREATE TABLE IF NOT EXISTS ingestion_audit (
    id SERIAL PRIMARY KEY,
    source_file VARCHAR(128) NOT NULL,
    accepted INTEGER NOT NULL DEFAULT 0,
    rejected INTEGER NOT NULL DEFAULT 0,
    corrected INTEGER NOT NULL DEFAULT 0,
    processed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);

-- 7. Rôles et permissions RBAC
CREATE TABLE IF NOT EXISTS roles (
    role_name VARCHAR(64) PRIMARY KEY,
    description TEXT,
    allowed_tools TEXT,
    can_confirm_action BOOLEAN DEFAULT FALSE
);

-- Index pour optimiser les requêtes fréquentes
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_priority ON tickets(priority);
CREATE INDEX IF NOT EXISTS idx_tickets_hostname ON tickets(hostname);
CREATE INDEX IF NOT EXISTS idx_service_checks_hostname ON service_checks(hostname, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_events_hostname_level ON events(hostname, level, timestamp DESC);
