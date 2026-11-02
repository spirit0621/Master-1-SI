"""
Tests d'intégration pour l'API Métier FastAPI
"""
import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from api.main import app

client = TestClient(app)

def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "UP"
    assert "database" in data

def test_get_tickets():
    response = client.get("/tickets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_ticket_creation_and_retrieval():
    payload = {
        "title": "Incident test automatisé",
        "hostname": "SRV-TEST-01",
        "priority": "HIGH",
        "description": "Validation du test unitaire"
    }
    create_resp = client.post("/tickets", json=payload)
    assert create_resp.status_code == 201
    created_ticket = create_resp.json()
    assert created_ticket["title"] == payload["title"]
    assert created_ticket["priority"] == "HIGH"
    assert "id" in created_ticket
