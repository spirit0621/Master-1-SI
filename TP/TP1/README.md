# Travaux Pratiques N°1 : API REST, HTTP et MCP (TECHCORP)

**Formation :** Master 1 Architecture des SI (CFA-INSTA)
**Module :** IA, API & MCP
**Dossier :** `TP1`

---

## 📑 Sommaire des Fichiers du Dossier

| Fichier | Description |
| :--- | :--- |
| 📘**[GUIDE_ETAPES_TP1_API_HTTP_MCP.md](./doc/GUIDE_ETAPES_TP1_API_HTTP_MCP.md)** | **Guide pas-à-pas complet :** Les 5 étapes de réalisation, commandes, tableaux complétés, réponses rédigées aux questions d'analyse (6.1, 6.2, 8.1, 10.1, 11.1), schéma final et questions flash pour l'oral. |
| 📝**[COMPTE_RENDU_TP1_QUESTIONS_REPONSES.md](./doc/COMPTE_RENDU_TP1_QUESTIONS_REPONSES.md)** | **Compte-rendu des questions/réponses :** Détail de l'ensemble des réponses théoriques et pratiques du TP. |
| 📄[TP1_CFA_INSTA_API_HTTP_MCP_3h_NB_FINAL.pdf](./TP1_CFA_INSTA_API_HTTP_MCP_3h_NB_FINAL.pdf) | **Sujet officiel du TP :** Document PDF remis par l'enseignant au CFA-INSTA. |
| ⚙️[server.py](./server.py) | **Serveur MCP (FastMCP) :** Implémentation du serveur Python exposant les tools `get_server_status` et `list_open_servers` pour MCP Inspector. |
| 🌐[api/app.py](./api/app.py) | **API REST (FastAPI) :** Implémentation des routes `GET /tickets`, `GET /status/open` et `POST /tickets`. |
| 📦[requirements.txt](./requirements.txt) | **Dépendances :** Bibliothèques Python nécessaires (`fastapi`, `uvicorn`, `mcp[cli]`). |

---

## 🚀 Commandes de Démarrage Rapide

```powershell
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'API FastAPI (Parties A et B)
uvicorn api.app:app --reload --port 8000

# 3. Lancer le serveur MCP dans l'Inspector (Partie C)
mcp dev server.py
```
