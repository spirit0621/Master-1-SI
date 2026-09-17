from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="TECHCORP Ticketing API",
    description="API de gestion des incidents et serveurs TECHCORP (TP1 CFA-INSTA)",
    version="1.0.0"
)

# Jeu de données simulé
SERVERS = {
    "SRV-DB-01": {"ip": "10.10.20.10", "role": "Database", "status": "UP"},
    "SRV-WEB-01": {"ip": "10.10.20.20", "role": "Web", "status": "DEGRADED"},
    "SRV-DNS-01": {"ip": "10.10.20.53", "role": "DNS", "status": "DOWN"}
}

TICKETS = [
    {"id": 1, "title": "DNS indisponible", "server": "SRV-DNS-01", "priority": "CRITICAL", "status": "OPEN"},
    {"id": 2, "title": "Latence application", "server": "SRV-WEB-01", "priority": "HIGH", "status": "OPEN"},
    {"id": 3, "title": "Mise à jour PostgreSQL", "server": "SRV-DB-01", "priority": "MEDIUM", "status": "CLOSED"},
    {"id": 4, "title": "Certificat à renouveler", "server": "SRV-WEB-01", "priority": "HIGH", "status": "OPEN"},
    {"id": 5, "title": "Contrôle sauvegarde nocturne", "server": "SRV-DB-01", "priority": "LOW", "status": "OPEN"}
]

# Modèle de validation Pydantic pour le POST
class TicketCreate(BaseModel):
    title: str
    server: str
    priority: str

@app.get("/")
def read_root():
    """Page d'accueil et documentation de l'API TECHCORP."""
    return {
        "message": "Bienvenue sur l'API TECHCORP (TP1 CFA-INSTA)",
        "docs_url": "http://127.0.0.1:8000/docs",
        "endpoints": [
            {"method": "GET", "path": "/tickets", "desc": "Tous les tickets"},
            {"method": "GET", "path": "/status/open", "desc": "Tickets ouverts"},
            {"method": "POST", "path": "/tickets", "desc": "Créer un ticket"}
        ]
    }

@app.get("/tickets", response_model=List[dict])
def get_all_tickets():
    """Endpoint A1 : Récupérer tous les tickets d'incident."""
    return TICKETS

@app.get("/status/open", response_model=List[dict])
def get_open_tickets():
    """Endpoint A2 : Lister uniquement les tickets ouverts."""
    return [t for t in TICKETS if t["status"] == "OPEN"]

@app.post("/tickets", status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate):
    """Endpoint A3 : Créer un nouveau ticket d'incident."""
    new_id = max([t["id"] for t in TICKETS], default=0) + 1
    new_ticket = {
        "id": new_id,
        "title": ticket.title,
        "server": ticket.server,
        "priority": ticket.priority,
        "status": "OPEN"
    }
    TICKETS.append(new_ticket)
    return new_ticket
