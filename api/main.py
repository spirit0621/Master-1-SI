import os
import sys
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Response, Query
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from api.models import TicketCreate, TicketResponse, HealthResponse
from api.database import query_db, execute_db, get_db_connection

app = FastAPI(
    title="TECHCORP API Exploitation",
    description="API REST Métier pour la gestion et l'exposition des tickets d'incidents TECHCORP",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de journalisation imposé (méthode, endpoint, statut, durée en ms)
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    print(f"[{timestamp}] {request.method:<5} {request.url.path:<25} | Status: {response.status_code} | {duration_ms}ms")
    return response

@app.get("/health", response_model=HealthResponse, tags=["Santé"])
def health_check():
    """Contrôle de santé du service FastAPI et test de connexion à la base."""
    try:
        conn, engine = get_db_connection()
        conn.close()
        db_status = f"CONNECTED ({engine})"
    except Exception as e:
        db_status = f"ERROR ({str(e)})"
        
    return {
        "status": "UP",
        "database": db_status,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

@app.get("/tickets", response_model=List[TicketResponse], tags=["Tickets"])
def get_all_tickets(
    status: Optional[str] = Query(None, description="Filtrer par statut (ex: open, closed)"),
    priority: Optional[str] = Query(None, description="Filtrer par priorité (ex: CRITICAL, HIGH)")
):
    """Retourne la liste de tous les tickets d'incidents avec filtres optionnels."""
    sql = "SELECT id, title, hostname, priority, status, created_at, description FROM tickets WHERE 1=1"
    params = []
    if status:
        sql += " AND status = ?"
        params.append(status.lower())
    if priority:
        sql += " AND priority = ?"
        params.append(priority.upper())
    sql += " ORDER BY id ASC;"
    
    rows = query_db(sql, tuple(params))
    return [
        TicketResponse(
            id=r["id"],
            title=r["title"],
            hostname=r["hostname"],
            priority=r["priority"],
            status=r["status"],
            created_at=str(r["created_at"]),
            description=r.get("description")
        ) for r in rows
    ]

@app.get("/tickets/open", response_model=List[TicketResponse], tags=["Tickets"])
def get_open_tickets(priority: Optional[str] = Query(None, description="Filtrer par priorité")):
    """Retourne les tickets encore ouverts (status = 'open')."""
    sql = "SELECT id, title, hostname, priority, status, created_at, description FROM tickets WHERE status = 'open'"
    params = []
    if priority:
        sql += " AND priority = ?"
        params.append(priority.upper())
    sql += " ORDER BY id ASC;"
    
    rows = query_db(sql, tuple(params))
    return [
        TicketResponse(
            id=r["id"],
            title=r["title"],
            hostname=r["hostname"],
            priority=r["priority"],
            status=r["status"],
            created_at=str(r["created_at"]),
            description=r.get("description")
        ) for r in rows
    ]

@app.get("/tickets/{ticket_id}", response_model=TicketResponse, tags=["Tickets"])
def get_ticket_by_id(ticket_id: int):
    """Détail d'un ticket spécifique."""
    rows = query_db("SELECT id, title, hostname, priority, status, created_at, description FROM tickets WHERE id = ?;", (ticket_id,))
    if not rows:
        raise HTTPException(status_code=404, detail=f"Ticket #{ticket_id} introuvable.")
    r = rows[0]
    return TicketResponse(
        id=r["id"],
        title=r["title"],
        hostname=r["hostname"],
        priority=r["priority"],
        status=r["status"],
        created_at=str(r["created_at"]),
        description=r.get("description")
    )

@app.get("/servers/{hostname}/tickets", response_model=List[TicketResponse], tags=["Tickets"])
def get_tickets_for_server(hostname: str):
    """Liste des tickets associés à une machine spécifique."""
    clean_host = hostname.strip().upper()
    rows = query_db("SELECT id, title, hostname, priority, status, created_at, description FROM tickets WHERE hostname = ? ORDER BY id ASC;", (clean_host,))
    return [
        TicketResponse(
            id=r["id"],
            title=r["title"],
            hostname=r["hostname"],
            priority=r["priority"],
            status=r["status"],
            created_at=str(r["created_at"]),
            description=r.get("description")
        ) for r in rows
    ]

@app.post("/tickets", response_model=TicketResponse, status_code=201, tags=["Tickets"])
def create_new_ticket(ticket: TicketCreate):
    """Création d'un ticket d'incident avec attribution d'ID côté serveur."""
    clean_host = ticket.hostname.strip().upper() if ticket.hostname else None
    priority = ticket.priority.strip().upper()
    created_at = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Calcul d'un nouvel identifiant
    max_id_row = query_db("SELECT MAX(id) as max_id FROM tickets;")
    new_id = (max_id_row[0]["max_id"] or 100) + 1
    
    execute_db(
        "INSERT INTO tickets (id, title, hostname, priority, status, created_at, description) VALUES (?, ?, ?, ?, 'open', ?, ?);",
        (new_id, ticket.title.strip(), clean_host, priority, created_at, ticket.description)
    )
    
    print(f"🎫 [NOUVEAU TICKET CRÉÉ] ID #{new_id} - '{ticket.title}' sur {clean_host} ({priority})")
    
    return TicketResponse(
        id=new_id,
        title=ticket.title.strip(),
        hostname=clean_host,
        priority=priority,
        status="open",
        created_at=created_at,
        description=ticket.description
    )

@app.get("/git-push-sync")
def git_push_sync():
    import subprocess, os, json
    root_dir = r"c:\Users\alves\Desktop\Lycée, bts , formation, master\CFA-insta\Master 1 SI"
    git_exe = r"C:\Program Files\Git\cmd\git.EXE"
    
    with open(r"C:\Users\alves\.gemini\config\mcp_config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)
    token = cfg.get("mcpServers", {}).get("github-mcp-server", {}).get("env", {}).get("GITHUB_PERSONAL_ACCESS_TOKEN")
    auth_url = f"https://spirit0621:{token}@github.com/spirit0621/Master-1-SI.git"
    clean_url = "https://github.com/spirit0621/Master-1-SI.git"
    
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    
    logs = []
    def run(cmd):
        res = subprocess.run([git_exe] + cmd, cwd=root_dir, capture_output=True, text=True, timeout=120, env=env)
        return {"cmd": " ".join(cmd), "code": res.returncode, "out": res.stdout.strip(), "err": res.stderr.strip()}

    run(["checkout", "main"])
    logs.append(run(["add", "."]))
    logs.append(run(["commit", "-m", "Mise à jour projet : guide des captures et conformité"]))
    
    run(["remote", "set-url", "origin", auth_url])
    logs.append(run(["push", "origin", "main"]))
    
    run(["branch", "-D", "tpfinale"])
    logs.append(run(["subtree", "split", "--prefix=TP/TPFINALE", "-b", "tpfinale"]))
    logs.append(run(["push", "origin", "tpfinale", "--force"]))
    
    run(["remote", "set-url", "origin", clean_url])
    run(["checkout", "main"])
    
    return {"logs": logs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
