# 🛠️ FAQ & Guide de Dépannage Développeur TECHCORP

Ce guide recense les erreurs les plus récurrentes rencontrées par les développeurs TECHCORP et les démarches de résolution associées.

## 1. Erreur HTTP 422 Unprocessable Entity
- **Cause :** Un payload JSON envoyé à un endpoint FastAPI ne correspond pas au schéma Pydantic attendu (champ manquant, mauvais type, format de date non ISO, ou valeur non permise par l'enum).
- **Procédure de résolution :**
  1. Consulter le corps de la réponse JSON retourné par l'API : le champ `detail` indique précisément le nom du champ en faute et la raison (`missing`, `value_error`, etc.).
  2. Comparer le JSON envoyé avec la documentation Swagger interactive sur `http://localhost:8000/docs`.
  3. Vérifier que les en-têtes de requête contiennent bien `Content-Type: application/json`.

## 2. Erreur CORS (Cross-Origin Resource Sharing)
- **Symptôme :** Le navigateur bloque la requête d'une application frontend vers l'API avec le message *No 'Access-Control-Allow-Origin' header is present*.
- **Solution :** Ajouter le middleware `CORSMiddleware` dans le fichier `api/app.py` :
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://internal.techcorp.lan:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 3. Ollama / Open WebUI : "Connection Refused" sur port 11434
- **Cause :** Le service Ollama n'écoute que sur `127.0.0.1` ou le conteneur Open WebUI ne parvient pas à résoudre l'hôte Ollama.
- **Solution :**
  1. Si Ollama tourne sur la machine hôte et Open WebUI dans Docker, définir l'environnement `OLLAMA_BASE_URL=http://host.docker.internal:11434` et ajouter `--add-host=host.docker.internal:host-gateway`.
  2. Si les deux tournent dans le même Docker Compose, définir `OLLAMA_BASE_URL=http://ollama:11434` et vérifier que le service s'appelle bien `ollama`.
