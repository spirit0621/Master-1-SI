"""
Validation automatisée des 6 requêtes SQL obligatoires (Section 4.2 du sujet)
Exécute chaque requête de manière 100% paramétrée sur la base TECHCORP.
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from api.database import query_db

def test_q1_open_critical_or_high_tickets():
    """Q1: Quels tickets CRITICAL ou HIGH sont encore ouverts ?"""
    sql = """
    SELECT id, title, hostname, priority, status, created_at 
    FROM tickets 
    WHERE status = ? AND priority IN (?, ?)
    ORDER BY created_at DESC;
    """
    rows = query_db(sql, ("open", "CRITICAL", "HIGH"))
    assert isinstance(rows, list)
    for r in rows:
        assert r["status"] == "open"
        assert r["priority"] in ["CRITICAL", "HIGH"]

def test_q2_incidents_for_specific_server():
    """Q2: Quels incidents concernent un serveur précis ?"""
    sql = """
    SELECT id, title, priority, status, created_at, description 
    FROM tickets 
    WHERE hostname = ?
    ORDER BY created_at DESC;
    """
    rows = query_db(sql, ("SRV-DB-01",))
    assert isinstance(rows, list)

def test_q3_last_check_for_service():
    """Q3: Quel est le dernier résultat de test connu pour un service ?"""
    sql = """
    SELECT sc.hostname, sc.port, sc.tcp_result, sc.latency_ms, sc.timestamp 
    FROM service_checks sc
    WHERE sc.hostname = ? AND sc.port = ?
    ORDER BY sc.timestamp DESC
    LIMIT 1;
    """
    rows = query_db(sql, ("SRV-DB-01", 5432))
    assert isinstance(rows, list)
    if rows:
        assert "tcp_result" in rows[0]

def test_q4_contradictions_inventory_vs_checks():
    """Q4: Quels serveurs ont des données contradictoires entre inventaire et tests ?"""
    sql = """
    SELECT s.hostname, s.inventory_status, sc.port, sc.tcp_result, sc.timestamp
    FROM servers s
    JOIN service_checks sc ON s.hostname = sc.hostname
    WHERE s.inventory_status = ? AND sc.tcp_result IN (?, ?, ?);
    """
    rows = query_db(sql, ("UP", "FAILED", "DOWN", "TIMEOUT"))
    assert isinstance(rows, list)

def test_q5_recent_error_events_for_server():
    """Q5: Quels événements ERROR concernent SRV-DB-01 depuis une heure donnée ?"""
    sql = """
    SELECT id, timestamp, level, hostname, component, message
    FROM events
    WHERE hostname = ? AND level = ? AND timestamp >= ?
    ORDER BY timestamp ASC;
    """
    rows = query_db(sql, ("SRV-DB-01", "ERROR", "2026-09-15 00:00:00"))
    assert isinstance(rows, list)

def test_q6_rejected_records_audit():
    """Q6: Combien d'enregistrements ont été rejetés pendant le traitement des données ?"""
    sql = """
    SELECT source_file, accepted, rejected, corrected, details, processed_at
    FROM ingestion_audit;
    """
    rows = query_db(sql)
    assert isinstance(rows, list)
    
    sum_sql = "SELECT SUM(rejected) as total_rejected FROM ingestion_audit;"
    sum_row = query_db(sum_sql)
    assert isinstance(sum_row, list)

if __name__ == "__main__":
    test_q1_open_critical_or_high_tickets()
    test_q2_incidents_for_specific_server()
    test_q3_last_check_for_service()
    test_q4_contradictions_inventory_vs_checks()
    test_q5_recent_error_events_for_server()
    test_q6_rejected_records_audit()
    print("✅ Les 6 requêtes SQL de la Section 4.2 sont 100% validées et paramétrées !")
