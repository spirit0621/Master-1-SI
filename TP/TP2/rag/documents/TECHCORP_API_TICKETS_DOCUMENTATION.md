# 📋 Spécification Officielle de l'API Tickets TECHCORP (v2.1)

Cette documentation interne décrit les points d'entrée (endpoints) du service de gestion des incidents et tickets techniques de TECHCORP.

## Informations Générales
- **Hôte de développement :** `http://localhost:8000`
- **Hôte de staging :** `http://api-staging.internal.techcorp.lan:8000`
- **Préfixe global des routes :** `/api/v1`
- **Format d'échange :** `application/json`
- **Authentification :** En-tête HTTP `Authorization: Bearer <TECHCORP_TOKEN>`

---

## 1. Lister les tickets ouverts
- **Méthode :** `GET`
- **Route :** `/api/v1/tickets`
- **Paramètres de requête (Query params) :**
  - `status` (optionnel) : `open`, `in_progress`, `closed` (défaut : `open`)
  - `limit` (optionnel) : entier entre 1 et 100 (défaut : 20)
- **Réponse succès (200 OK) :**
```json
[
  {
    "id": "TCK-1042",
    "title": "Erreur 500 sur le service d'authentification",
    "priority": "P1-CRITICAL",
    "service": "auth-service",
    "status": "open",
    "assignee": "team-secops",
    "created_at": "2026-09-15T08:30:00Z"
  }
]
```

---

## 2. Créer un nouveau ticket d'incident
- **Méthode :** `POST`
- **Route :** `/api/v1/tickets`
- **En-têtes requis :** `Content-Type: application/json`
- **Corps de la requête (JSON Body) :**
```json
{
  "title": "Panne de connectivité base PostgreSQL",
  "description": "Les microservices retournent ConnectionRefusedError sur le port 5432.",
  "priority": "P2-HIGH",
  "service": "billing-api",
  "environment": "staging"
}
```
- **Règles de validation Pydantic :**
  - `title` : chaîne non vide, max 120 caractères.
  - `priority` : valeurs admises `P1-CRITICAL`, `P2-HIGH`, `P3-MEDIUM`, `P4-LOW`.
  - `environment` : valeurs admises `development`, `staging`, `production`.
- **Réponse succès (201 Created) :**
```json
{
  "id": "TCK-1043",
  "title": "Panne de connectivité base PostgreSQL",
  "status": "open",
  "created_at": "2026-09-15T10:15:22Z"
}
```
- **Erreurs possibles :**
  - `400 Bad Request` : Si le service mentionné n'est pas répertorié dans le catalogue TECHCORP.
  - `422 Unprocessable Entity` : Si l'un des champs ne respecte pas le type ou la liste de valeurs autorisées.

---

## 3. Consulter l'état des serveurs de production
- **Méthode :** `GET`
- **Route :** `/api/v1/servers/status`
- **Description :** Retourne la santé de tous les nœuds de production (CPU, RAM, statut).
