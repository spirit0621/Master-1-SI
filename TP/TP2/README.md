# 🎓 TP FIL ROUGE : Assistant IA Métier Local (TECHCORP)

**Formation :** Master 1 Architecture des SI (CFA-INSTA)  
**Module :** IA, API & MCP  
**Profil retenu :** Développement Applicatif (DevAssist-GPT)  
**Dossier :** `TP2`

---

## 📑 Sommaire des Fichiers et Livrables du Projet

| Fichier / Dossier | Rôle & Description |
| :--- | :--- |
| 📘 **[TP2_FIL_ROUGE_ASSISTANT_IA_LOCAL_REPONSES_COMPLETES.md](./TP2_FIL_ROUGE_ASSISTANT_IA_LOCAL_REPONSES_COMPLETES.md)** | **Compte-rendu intégral :** Chaque étape, consigne et question du sujet PDF avec sa réponse détaillée, tableaux complétés, diagnostics et questions de soutenance. |
| 📊 **[dataset/dataset.json](./dataset/dataset.json)** | **Dataset d'entraînement (60 exemples) :** Paires instruction/réponse réparties en fondamentaux, procédures, diagnostics d'erreurs (422, CORS) et cas de transparence/inconnu. |
| 🧠 **[model/Modelfile](./model/Modelfile)** | **Configuration Ollama :** Prompt SYSTEM spécialisé TECHCORP, paramètres d'inférence (`temperature 0.2`, `top_p 0.9`, `repeat_penalty 1.1`, `num_ctx 4096`). |
| 📚 **[rag/documents/](./rag/documents/)** | **Base de connaissances RAG (4 documents) :** Spécification OpenAPI Tickets, Conventions PEP 8 TECHCORP, Guide Docker et FAQ Dépannage. |
| 🐳 **[deploy/compose.yml](./deploy/compose.yml)** | **Déploiement conteneurisé :** Orchestration Docker Compose pour Ollama et Open WebUI avec volumes de persistance. |
| 📝 **[bilan.md](./bilan.md)** | **Bilan d'une page :** Analyse des réussites, limites constatées, pannes rencontrées et axes d'amélioration. |
| 📄 **[TP_Fil_Rouge_Assistant_IA_Local_NB_Dev.pdf](./TP_Fil_Rouge_Assistant_IA_Local_NB_Dev.pdf)** | **Sujet officiel du TP :** Énoncé fourni par l'enseignant au CFA-INSTA. |

---

## 🚀 Démarrage Rapide

### 1. Démarrage de l'infrastructure Docker (VM ou local)
```bash
cd deploy
docker compose up -d
docker compose ps
```

### 2. Compilation de l'assistant spécialisé dans Ollama
```bash
docker exec -it ollama ollama pull qwen2.5:7b
docker exec -it ollama ollama create devassist-gpt -f /workspace/Modelfile
```

### 3. Connexion à l'interface graphique
Ouvrez votre navigateur sur : `http://localhost:3000` (ou `http://<IP_VM>:3000`).
