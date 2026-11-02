from typing import Optional
from pydantic import BaseModel, Field

class TicketCreate(BaseModel):
    title: str = Field(..., description="Titre descriptif de l'incident")
    hostname: Optional[str] = Field(None, description="Nom de la machine concernée (ex: SRV-DB-01)")
    priority: str = Field("MEDIUM", description="Niveau de priorité : CRITICAL, HIGH, MEDIUM, LOW")
    description: Optional[str] = Field(None, description="Détails techniques de l'incident")

class TicketResponse(BaseModel):
    id: int
    title: str
    hostname: Optional[str]
    priority: str
    status: str
    created_at: str
    description: Optional[str]

class HealthResponse(BaseModel):
    status: str
    database: str
    timestamp: str
