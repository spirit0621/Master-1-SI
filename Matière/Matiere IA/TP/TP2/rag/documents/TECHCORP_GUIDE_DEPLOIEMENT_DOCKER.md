# 🐳 Guide de Déploiement Conteneurisé TECHCORP (Docker & Compose)

Ce document décrit les règles et commandes standards pour conteneuriser et déployer une application sur l'infrastructure interne de TECHCORP (VMs Linux ESXi).

## 1. Dockerfile Standard FastAPI
Tout service Python TECHCORP doit respecter la structure multi-stage suivante pour réduire la taille de l'image et renforcer la sécurité :

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS runner
WORKDIR /app
# Sécurité : création d'un utilisateur non-root
RUN addgroup --system techcorp && adduser --system --group techcorp
COPY --from=builder /root/.local /home/techcorp/.local
COPY . /app
USER techcorp
ENV PATH=/home/techcorp/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 2. Règles de déploiement en environnement de recette/production
- **Ports réservés chez TECHCORP :**
  - `3000` : Interface Web Open WebUI / Dashboards internes.
  - `8000` : APIs applicatives FastAPI principales.
  - `11434` : Moteur d'IA local Ollama.
  - `5432` : Bases de données PostgreSQL internes.
- **Réseau interne :**
  Les conteneurs interconnectés doivent impérativement partager un réseau bridge Docker dédié (ex: `techcorp-network`).
- **Persistance :**
  Ne jamais stocker de données d'état (bases de données, fichiers uploadés, modèles LLM) dans la couche volatile d'un conteneur. Utiliser des volumes nommés déclarés dans `compose.yml`.
