"""
Serveur MCP Python (FastMCP) pour TECHCORP
TP1 — CFA-INSTA : Découverte du Model Context Protocol (MCP)
"""

from mcp.server.fastmcp import FastMCP

# 1. Initialisation du serveur MCP nommé TechCorp
mcp = FastMCP("TechCorp")

# 2. Jeu de données métier simulé
SERVERS = {
    "SRV-DB-01": {"ip": "10.10.20.10", "role": "Database", "status": "UP"},
    "SRV-WEB-01": {"ip": "10.10.20.20", "role": "Web", "status": "DEGRADED"},
    "SRV-DNS-01": {"ip": "10.10.20.53", "role": "DNS", "status": "DOWN"}
}

# 3. Tool principal demandé dans le TP
@mcp.tool()
def get_server_status(hostname: str) -> dict:
    """Retourne l'état opérationnel et les caractéristiques d'un serveur TECHCORP."""
    hostname = hostname.upper().strip()
    if hostname not in SERVERS:
        return {"success": False, "error": f"Serveur '{hostname}' inconnu dans le parc TECHCORP"}
    
    return {
        "success": True,
        "hostname": hostname,
        **SERVERS[hostname]
    }

# 4. Extension Bonus (Section 10.3 du TP)
@mcp.tool()
def list_open_servers() -> dict:
    """Retourne uniquement la liste des serveurs dont l'état n'est pas DOWN."""
    operational_servers = {
        h: data for h, data in SERVERS.items() if data["status"] != "DOWN"
    }
    return {
        "success": True,
        "count": len(operational_servers),
        "servers": operational_servers
    }

if __name__ == "__main__":
    mcp.run()
