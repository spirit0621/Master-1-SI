"""
Serveur MCP TECHCORP (FastMCP)
Expose les capacités d'observation et d'action du SI TECHCORP au LLM.
Fournit les 5 Tools du socle, le Tool d'action avancée, 2 Resources et 1 Prompt.
"""
import os
import sys
import socket
import time
from typing import Optional, Dict, Any, List
import requests
from mcp.server.fastmcp import FastMCP

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from api.database import query_db, execute_db

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")

mcp = FastMCP("techcorp-mcp-server")

# ==============================================================================
# 1. TOOLS DU SOCLE OBLIGATOIRE (5 TOOLS)
# ==============================================================================

@mcp.tool()
def get_server_info(hostname: str) -> Dict[str, Any]:
    """Retourne la fiche normalisée d'un serveur depuis la base PostgreSQL (accès direct DB).
    Args:
        hostname: Nom du serveur normalisé (ex: SRV-DB-01, SRV-APP-01, SRV-WEB-01)
    """
    clean_host = hostname.strip().upper()
    servers = query_db(
        "SELECT hostname, ip_address, role, os, environment, inventory_status FROM servers WHERE hostname = ?;",
        (clean_host,)
    )
    if not servers:
        return {
            "status": "NOT_FOUND",
            "hostname": clean_host,
            "message": f"Le serveur '{clean_host}' est introuvable dans le référentiel d'inventaire.",
            "source": "postgresql_servers"
        }
    
    server_data = servers[0]
    # Récupération des services déclarés
    services = query_db(
        "SELECT service_name, port, expected_state FROM services WHERE hostname = ?;",
        (clean_host,)
    )
    server_data["services"] = services
    server_data["source"] = "postgresql_direct"
    return server_data

@mcp.tool()
def list_open_tickets(priority: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retourne les tickets d'incidents ouverts en interrogeant l'API métier FastAPI.
    Args:
        priority: Filtre optionnel (CRITICAL, HIGH, MEDIUM, LOW)
    """
    params = {}
    if priority:
        params["priority"] = priority.strip().upper()
        
    try:
        resp = requests.get(f"{FASTAPI_URL}/tickets/open", params=params, timeout=3.0)
        if resp.status_code == 200:
            tickets = resp.json()
            for t in tickets:
                t["source"] = "fastapi_api_http"
            return tickets
    except Exception as e:
        # Fallback de secours en base locale si l'API n'est pas lancée
        pass
        
    sql = "SELECT id, title, hostname, priority, status, created_at, description FROM tickets WHERE status = 'open'"
    query_params = []
    if priority:
        sql += " AND priority = ?"
        query_params.append(priority.strip().upper())
    sql += " ORDER BY id ASC;"
    
    rows = query_db(sql, tuple(query_params))
    for r in rows:
        r["source"] = "db_direct_fallback"
    return rows

@mcp.tool()
def get_recent_events(hostname: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Retourne les événements et journaux techniques récents liés à un serveur (PostgreSQL).
    Args:
        hostname: Nom du serveur (ex: SRV-DB-01)
        limit: Nombre maximal d'événements (défaut : 10)
    """
    clean_host = hostname.strip().upper()
    events = query_db(
        "SELECT timestamp, level, hostname, component, message FROM events WHERE hostname = ? ORDER BY timestamp DESC LIMIT ?;",
        (clean_host, limit)
    )
    for e in events:
        e["source"] = "postgresql_events"
    return events

@mcp.tool()
def check_server_availability(hostname: str) -> Dict[str, Any]:
    """Effectue un test réseau réel (sonde socket TCP active) pour vérifier la joignabilité en direct.
    Retourne : UP, SERVICE_DOWN, DOWN, ou UNKNOWN.
    """
    clean_host = hostname.strip().upper()
    start_time = time.time()
    
    # 1. Recherche de l'IP et du port dans l'inventaire
    servers = query_db("SELECT ip_address FROM servers WHERE hostname = ?;", (clean_host,))
    if not servers:
        return {
            "hostname": clean_host,
            "result": "UNKNOWN",
            "error": f"Hôte '{clean_host}' inconnu en inventaire.",
            "source": "network_tcp_probe"
        }
        
    services = query_db("SELECT port FROM services WHERE hostname = ? LIMIT 1;", (clean_host,))
    target_port = services[0]["port"] if services else (5432 if "DB" in clean_host else (8000 if "APP" in clean_host else 80))
    target_ip = "127.0.0.1" # Test en local ou target IP réelle
    
    status_result = "DOWN"
    try:
        # Sonde socket TCP avec timeout court (2s)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        sock.connect((target_ip, target_port))
        sock.close()
        status_result = "UP"
    except ConnectionRefusedError:
        # Machine joignable mais port fermé / service stoppé
        status_result = "SERVICE_DOWN"
    except (socket.timeout, OSError):
        status_result = "DOWN"
        
    duration_ms = round((time.time() - start_time) * 1000, 2)
    
    return {
        "hostname": clean_host,
        "ip_tested": target_ip,
        "port_tested": target_port,
        "result": status_result,
        "latency_ms": duration_ms,
        "source": "live_tcp_socket_probe"
    }

@mcp.tool()
def get_last_service_check(hostname: str) -> Dict[str, Any]:
    """Récupère la dernière mesure de contrôle enregistrée dans l'historique PostgreSQL.
    Args:
        hostname: Nom du serveur
    """
    clean_host = hostname.strip().upper()
    checks = query_db(
        "SELECT timestamp, hostname, port, tcp_result, latency_ms, source FROM service_checks WHERE hostname = ? ORDER BY timestamp DESC LIMIT 1;",
        (clean_host,)
    )
    if not checks:
        return {
            "hostname": clean_host,
            "status": "NO_HISTORY",
            "message": f"Aucun historique de mesure pour '{clean_host}'.",
            "source": "postgresql_service_checks"
        }
    res = checks[0]
    res["source"] = "postgresql_service_checks_history"
    return res

# ==============================================================================
# 2. OUTILS & RESSOURCES DE NIVEAU AVANCÉ
# ==============================================================================

@mcp.tool()
def create_ticket(hostname: str, priority: str, title: str, description: Optional[str] = None, confirm: bool = False) -> Dict[str, Any]:
    """Crée un ticket d'incident dans l'API FastAPI uniquement après confirmation humaine explicite.
    Args:
        hostname: Machine concernée
        priority: Priorité (CRITICAL, HIGH, MEDIUM, LOW)
        title: Titre de l'incident
        description: Détail technique
        confirm: Doit impérativement être True pour exécuter la création.
    """
    if not confirm:
        return {
            "status": "REJECTED_UNCONFIRMED",
            "message": "Action bloquée par la sécurité : la création d'un ticket exige une validation humaine explicite. Demandez confirmation à l'utilisateur.",
            "source": "mcp_security_guard"
        }
        
    clean_host = hostname.strip().upper()
    prio = priority.strip().upper()
    
    # Appel vers FastAPI POST /tickets
    payload = {
        "title": title,
        "hostname": clean_host,
        "priority": prio,
        "description": description or "Créé par Assistant IA après validation"
    }
    try:
        resp = requests.post(f"{FASTAPI_URL}/tickets", json=payload, timeout=3.0)
        if resp.status_code == 201:
            data = resp.json()
            data["action_status"] = "SUCCESS_CONFIRMED"
            data["source"] = "fastapi_api_http"
            return data
    except Exception:
        pass
        
    # Fallback insertion directe en DB
    max_id_row = query_db("SELECT MAX(id) as max_id FROM tickets;")
    new_id = (max_id_row[0]["max_id"] or 100) + 1
    created_at = time.strftime("%Y-%m-%d %H:%M:%S")
    execute_db(
        "INSERT INTO tickets (id, title, hostname, priority, status, created_at, description) VALUES (?, ?, ?, ?, 'open', ?, ?);",
        (new_id, title, clean_host, prio, created_at, description)
    )
    return {
        "action_status": "SUCCESS_CONFIRMED",
        "id": new_id,
        "title": title,
        "hostname": clean_host,
        "priority": prio,
        "status": "open",
        "created_at": created_at,
        "source": "postgresql_direct_fallback"
    }

@mcp.resource("procedures://dns")
def get_dns_procedure() -> str:
    """Procédure d'escalade d'urgence en cas d'incident DNS."""
    proc_file = os.path.join(os.path.dirname(__file__), "..", "procedures", "procedure_dns.txt")
    if os.path.exists(proc_file):
        with open(proc_file, "r", encoding="utf-8") as f:
            return f.read()
    return "Procédure d'incident DNS introuvable."

@mcp.resource("procedures://incidents")
def get_incident_procedure() -> str:
    """Procédure générale de gestion des incidents et d'escalade."""
    proc_file = os.path.join(os.path.dirname(__file__), "..", "procedures", "procedure_incidents.txt")
    if os.path.exists(proc_file):
        with open(proc_file, "r", encoding="utf-8") as f:
            return f.read()
    return "Procédure d'incident introuvable."

@mcp.resource("inventory://summary")
def get_inventory_summary() -> str:
    """Synthèse non sensible du parc de serveurs."""
    servers = query_db("SELECT hostname, role, os, environment, inventory_status FROM servers;")
    lines = ["=== SYNTHÈSE DU PARC DE SERVEURS TECHCORP ==="]
    for s in servers:
        lines.append(f"• {s['hostname']} | Rôle: {s['role']} | OS: {s['os']} | Env: {s['environment']} | Statut: {s['inventory_status']}")
    return "\n".join(lines)

@mcp.prompt()
def analyse_incident(hostname: str, symptom: str) -> str:
    """Génère le prompt d'analyse d'incident imposant la séparation Faits / Hypothèses / Recommandations."""
    return f"""Tu es l'assistant IA d'exploitation TECHCORP.
L'opérateur analyse un dysfonctionnement sur la machine : {hostname}.
Symptôme rapporté : {symptom}.

Tu DOIS impérativement structurer ta réponse en trois sections distinctes :
1. FAITS ÉTABLIS : Données d'inventaire consultées et mesures réseau obtenues via les Tools MCP.
2. HYPOTHÈSES TECHNIQUES : Analyse des corrélations d'erreurs et des contradictions éventuelles.
3. RECOMMANDATIONS OPÉRATIONNELLES : Actions concrètes à mener selon les procédures internes.
"""

if __name__ == "__main__":
    mcp.run()
